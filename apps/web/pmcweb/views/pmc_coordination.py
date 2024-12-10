# -*- coding: utf-8 -*-
# @Time        : 2023/03/01
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Monitoring
# @Project     : GOC Automation Platform
import json
from resource_base.modules.importModules import *
from operator import itemgetter
from pmcweb.models import PMCAssignee, PMCActivities, PMCOperation, PMCDevicelist, PMCActivityplan, PMCBackupschedule
from userweb.models import Account
from mainweb.models import TimeSavingStatistics
from django.forms.models import model_to_dict
import logging
from operationweb.scripts import cmdb_request
from pmcweb.scripts import itsp_request
import csv
import requests
import pytz
from datetime import datetime
from pmcweb.scripts import backup_request

# Get the django logger
logger = logging.getLogger('django')


def pmc_new_request_index(request):
    """Return pmc new request page
        Args:
            request
        Returns:
            Render to pmc_new_request.html
    """
    return render(request, 'pmc/pmc_new_request.html')


def pmc_view_request_index(request):
    """Return pmc view request page
        Args:
            request
        Returns:
            Render to pmc_view_request.html
    """
    return render(request, 'pmc/pmc_view_request.html')


def pmc_edit_request_index(request):
    """Return pmc edit request page
            Args:
                request
            Returns:
                Render to pmc_edit_request.html
        """
    try:
        rec = request.GET

        pmc_activity = model_to_dict(PMCActivities.objects.get(pmc_id=rec.get('pmc_id')))
        pmc_confirmed = PMCOperation.objects.filter(pmc_id=rec.get('pmc_id'))
        if pmc_confirmed:
            pmc_activity['pmc_confirmed'] = '1'
        else:
            pmc_activity['pmc_confirmed'] = '0'

        pmc_activity['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pmc_activity['start_time'])) if pmc_activity['start_time'] else ''
        pmc_activity['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pmc_activity['end_time'])) if pmc_activity['end_time'] else ''

        pmc_activity_plan = list(PMCActivityplan.objects.filter(pmc_id=rec.get('pmc_id')).values())


    except Exception as e:
        logger.error('Error retrieving PMC activity: ' + str(e))

    return render(request, 'pmc/pmc_edit_request.html', {'pmc_activity': json.dumps(pmc_activity), 'pmc_activity_plan': json.dumps(pmc_activity_plan)})


def new_request_get_assignee(request):
    format_assignee_list = []

    try:
        pmc_assignee_list = list(PMCAssignee.objects.all().values())

        for assignee in pmc_assignee_list:
            assignee_name_with_department = assignee['assignee_name'] + ' (' + assignee['assignee_department'] + ')'
            assignee_responsible = assignee['assignee_responsible']

            format_assignee_list.append({'name': assignee_name_with_department, 'responsible': assignee_responsible})
    except Exception as e:
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True, 'data': format_assignee_list})


def new_request_get_pmc_coordinator(request):
    format_coordinator_list = []

    try:
        pmc_coordinator_list = list(Account.objects.filter(pmc_coordinator=1).values())

        for assignee in pmc_coordinator_list:
            assignee_name_with_department = assignee['name'] + ' (' + assignee['department'] + ')'
            format_coordinator_list.append(assignee_name_with_department)
    except Exception as e:
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True, 'data': format_coordinator_list})


def new_request_get_itsp_data(request):
    try:
        rec = request.POST
        itsp_number = rec.get('itspNumber')
        logger.info(request.session.get('user_account')['loginid'] + ' is retrieving ITSP data for: %s' % (str(itsp_number),))

        # Get ITSP data from API
        result_data = itsp_request.get_itsp_data(itsp_number, 'APAC\GPC1SZH', 'GOCAutomation2@24')

        logger.info('ITSP data: ' + str(result_data))
        if result_data == '401':
            return JsonResponse({'status': False, 'error': 'Access ITSP API failed, please check your credential.'})
        elif result_data == "403":
            return JsonResponse({'status': False, 'error': 'Access ITSP API denied, please check your role.'})
        elif result_data == "404":
            return JsonResponse({'status': False, 'error': 'ITSP number not exist, please check again.'})
    except Exception as e:
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True, 'data': result_data})


def new_request_save_activity_plan(request):

    try:
        rec = request.POST
        san_selection = rec.getlist('sanSelection')
        # pmc_activity_exist = PMCActivities.objects.filter(change_number=rec.get('changeNumber'), data_status=1)
        # if pmc_activity_exist:
        #     return JsonResponse({'status': False, 'error': 'The PMC activity already exist.'})

        # Initiate SAN properties
        if 'NO' in san_selection:
            san_vnx = '0'
            san_unity = '0'
            san_vplex = '0'
        elif 'TOBECHECKED' in san_selection:
            san_vnx = '2'
            san_unity = '2'
            san_vplex = '2'
        else:
            if 'VNX' in san_selection:
                san_vnx = '1'
            else:
                san_vnx = '0'

            if 'UNITY' in san_selection:
                san_unity = '1'
            else:
                san_unity = '0'

            if 'VPLEX' in san_selection:
                san_vplex = '1'
            else:
                san_vplex = '0'

        # Format the datetime
        pmc_start_time = time.strptime(rec.get('pmcStartTime'), "%Y-%m-%d %H:%M:%S")
        pmc_end_time = time.strptime(rec.get('pmcEndTime'), "%Y-%m-%d %H:%M:%S")

        pmc_activity = PMCActivities(
            itsp_no=rec.get('itspNumber'),
            data_status=1,
            data_center_room=rec.get('dataCenterRoom'),
            change_class=rec.get('changeClass'),
            reason=rec.get('reason'),
            start_time=int(time.mktime(pmc_start_time)),
            end_time=int(time.mktime(pmc_end_time)),
            start_with_shutdown=rec.get('startWithShutdown'),
            region=rec.get('region'),
            location_code=rec.get('locationCode'),
            additional_people=rec.get('additionalPeople'),
            people_onsite=rec.get('peopleOnSite'),
            engineer_address=rec.get('emailAddress'),
            contact_information=rec.get('contactInformation'),
            change_number=rec.get('changeNumber'),
            status=rec.get('pmcStatus'),
            power_off_assignee=rec.get('powerOffAssignee'),
            power_on_assignee=rec.get('powerOnAssignee'),
            san_vnx=san_vnx,
            san_unity=san_unity,
            san_vplex=san_vplex,
            nas=rec.get('nasSelection'),
            backup=rec.get('backupSelection'),
            oracle_db=rec.get('oracleDBSelection'),
            high_availability=rec.get('highAvailbilitySelection'),
            server_room_to_failover=rec.get('serverRoomToFailover'),
            service_to_failover=rec.get('serviceToFailover'),
            backup_assignee=rec.get('backupAssignee'),
            oracle_db_assignee=rec.get('oracleDBAssignee'),
            pmc_coordinator=rec.get('pmcCoordinator')
        )
        pmc_activity.save()
    except Exception as e:
        logger.error('Error saving PMC activity: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    # Time saving statistic
    TimeSavingStatistics.time_saving_statistic('pmc_coordination', 1350)
    return JsonResponse({'status': True, 'data': {'pmc_id': pmc_activity.pmc_id}})


def view_request_search_activity(request):
    try:
        rec = request.POST
        pmc_status = rec.getlist('searchPMCStatus')
        region = rec.get('searchRegion')
        location_code = rec.get('searchLocationCode')
        logger.info(request.session.get('user_account')['loginid'] + ' is searching PMC data for: %s %s %s' % (str(pmc_status), str(region), str(location_code)))

        if not pmc_status and not region and not location_code:
            pmc_activities = list(PMCActivities.objects.filter((Q(status__in=[0,1,2,3])), Q(data_status=1)).values())
        elif not pmc_status and (region or location_code):
            pmc_activities = list(PMCActivities.objects.filter(Q(status__in=[0,1,2,3,4,5]), Q(region__icontains=region), Q(location_code__icontains=location_code), Q(data_status=1)).values())
        else:
            pmc_activities = list(PMCActivities.objects.filter(Q(status__in=pmc_status), Q(region__icontains=region), Q(location_code__icontains=location_code), Q(data_status=1)).values())
        # Resort the attributes
        sorted_pmc_activities = []
        for activity in pmc_activities:
            # status: 0: New, 1: In progress, 2: Pending, 3: Scheduled, 4: Completed, 5: Cancelled
            if activity['status'] == 0:
                status = 'New'
            elif activity['status'] == 1:
                status = 'In progress'
            elif activity['status'] == 2:
                status = 'Pending'
            elif activity['status'] == 3:
                status = 'Scheduled'
            elif activity['status'] == 4:
                status = 'Completed'
            elif activity['status'] == 5:
                status = 'Cancelled'
            else:
                status = 'Unknown'

            # san: 0: No, 1: Yes, 2: To be checked
            if activity['san_vnx'] == 0 and activity['san_unity'] == 0 and activity['san_vplex'] == 0:
                san = 'No'
            elif activity['san_vnx'] == 2 and activity['san_unity'] == 2 and activity['san_vplex'] == 2:
                san = 'To be checked'
            else:
                san = 'Yes'

            # change_class: 0: class 0, 1: class 1, 2: class 2, 3: Emergency, 4: To be checked
            if activity['change_class'] == 0:
                change_class = '0'
            elif activity['change_class'] == 1:
                change_class = '1'
            elif activity['change_class'] == 2:
                change_class = '2'
            elif activity['change_class'] == 3:
                change_class = 'Emergency'
            elif activity['change_class'] == 4:
                change_class = 'To be checked'
            else:
                change_class = 'Unknown'

            activity_temp = {'pmc_id': activity['pmc_id'],
                             'change_number': activity['change_number'],
                             'region': activity['region'],
                             'location_code': activity['location_code'],
                             'data_center_room': activity['data_center_room'],
                             'status': status,
                             'start_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(activity['start_time'])) if activity['start_time'] else '-',
                             'end_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(activity['end_time'])) if activity['end_time'] else '-',
                             'san': san,
                             'change_class': change_class,
                             'pmc_coordinator': activity['pmc_coordinator'],
                             }

            sorted_pmc_activities.append(activity_temp)
            sorted_pmc_activities.sort(key=itemgetter('start_time'), reverse=True)

    except Exception as e:
        logger.error('Error searching PMC activities: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True, 'data': sorted_pmc_activities})


def view_request_delete_activity(request):
    try:
        rec = request.POST
        pmc_activity = PMCActivities.objects.get(pmc_id=rec.get('pmc_id'))

        if request.session.get('user_account')['guest_account'] == 1:
            return JsonResponse({'status': False, 'error': 'You don\'t have permission to delete requests.'})

        if pmc_activity:
            pmc_activity.data_status = 0
            pmc_activity.save()
        else:
            return JsonResponse({'status': False, 'error': 'PMC activity not found!'})
    except Exception as e:
        logger.error('Error deleting PMC activity: ' + str(e))
        return JsonResponse({'status': False, 'error': 'Error deleting PMC activity: ' + str(e)})

    return JsonResponse({'status': True})


def view_request_get_activity(request):
    try:
        rec = request.POST
        pmc_activity = model_to_dict(PMCActivities.objects.get(pmc_id=rec.get('pmc_id')))

        pmc_activity['start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pmc_activity['start_time'])) if pmc_activity['start_time'] else ''
        pmc_activity['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pmc_activity['end_time'])) if pmc_activity['end_time'] else ''

    except Exception as e:
        logger.error('Error retrieving PMC activity: ' + str(e))
        return JsonResponse({'status': False, 'error': 'Error retrieving PMC activity: ' + str(e)})

    return JsonResponse({'status': True, 'data': pmc_activity})


def edit_request_save_activity(request):
    try:
        rec = request.POST

        if request.session.get('user_account')['guest_account'] == 1:
            return JsonResponse({'status': False, 'error': 'You don\'t have permission to edit PMC requests.'})

        # Save to PMC Activity
        pmc_activity = PMCActivities.objects.get(pmc_id=rec.get('pmcID'))

        pmc_activity.data_center_room = rec.get('dataCenterRoom')
        pmc_activity.change_class = rec.get('changeClass')
        pmc_activity.start_time = int(time.mktime(time.strptime(rec.get('pmcStartTime'), "%Y-%m-%d %H:%M:%S")))
        pmc_activity.end_time = int(time.mktime(time.strptime(rec.get('pmcEndTime'), "%Y-%m-%d %H:%M:%S")))
        pmc_activity.start_with_shutdown = rec.get('startWithShutdown')
        pmc_activity.region = rec.get('region')
        pmc_activity.location_code = rec.get('locationCode')
        pmc_activity.additional_people = rec.get('additionalPeople')
        pmc_activity.people_onsite = rec.get('peopleOnSite')
        pmc_activity.engineer_address = rec.get('emailAddress')
        pmc_activity.contact_information = rec.get('contactInformation')
        pmc_activity.change_number = rec.get('changeNumber')
        pmc_activity.status = rec.get('pmcStatus')
        pmc_activity.power_off_assignee = rec.get('powerOffAssignee')
        pmc_activity.power_on_assignee = rec.get('powerOnAssignee')
        pmc_activity.nas = rec.get('nasSelection')
        pmc_activity.backup = rec.get('backupSelection')
        pmc_activity.oracle_db = rec.get('oracleDBSelection')
        pmc_activity.backup_assignee = rec.get('backupAssignee')
        pmc_activity.oracle_db_assignee = rec.get('oracleDBAssignee')
        pmc_activity.high_availability = rec.get('highAvailbilitySelection')
        pmc_activity.server_room_to_failover = rec.get('serverRoomToFailover')
        pmc_activity.service_to_failover = rec.get('serviceToFailover')
        pmc_activity.pmc_coordinator = rec.get('pmcCoordinator')
        pmc_activity.reason = rec.get('reason')

        if 'TOBECHECKED' in rec.getlist('sanSelection'):
            pmc_activity.san_vnx = 2
            pmc_activity.san_unity = 2
            pmc_activity.san_vplex = 2
        elif 'NO' in rec.getlist('sanSelection'):
            pmc_activity.san_vnx = 0
            pmc_activity.san_unity = 0
            pmc_activity.san_vplex = 0
        else:
            if 'VNX' in rec.getlist('sanSelection'):
                pmc_activity.san_vnx = 1
            else:
                pmc_activity.san_vnx = 0
            if 'UNITY' in rec.getlist('sanSelection'):
                pmc_activity.san_unity = 1
            else:
                pmc_activity.san_unity = 0
            if 'VPLEX' in rec.getlist('sanSelection'):
                pmc_activity.san_vplex = 1
            else:
                pmc_activity.san_vplex = 0
        # Update PMC Activity
        pmc_activity.save()

        # Save to PMC Activity Plan
        pmc_activity_plan = rec.get('pmcActivityPlan')

        pmc_activity_plan_br = pmc_activity_plan.replace('<br>', '').replace('\n', '')
        pmc_activity_plan = json.loads(pmc_activity_plan_br)

        # Delete old data before saving
        if PMCActivityplan.objects.filter(pmc_id=rec.get('pmcID')).exists():
            PMCActivityplan.objects.filter(pmc_id=rec.get('pmcID')).delete()

        for line_number, plan_data in enumerate(pmc_activity_plan):
            data_to_be_saved = PMCActivityplan(pmc_id=pmc_activity.pmc_id,
                                               line_number=line_number,
                                               date_start=plan_data['Date Start'],
                                               start_time=plan_data['Start time (UTC+0)'],
                                               description_of_activity=plan_data['Description of the activities'],
                                               execution=plan_data['Execution'],
                                               responsible=plan_data['Responsible Team/Person'],
                                               information_to=plan_data['Give Information To']
                                               )
            data_to_be_saved.save()

    except Exception as e:
        logger.error('Error saving PMC activity: ' + str(e))
        return JsonResponse({'status': False, 'error': 'Error saving PMC activity: ' + str(e)})

    return JsonResponse({'status': True})


def edit_request_get_device_list(request):
    rec = request.POST
    data_center_room = rec.get('dataCenterRoom').upper()

    device_list = cmdb_request.get_pmc_device_list(data_center_room)

    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=' + data_center_room + '.csv'

    # 导出excel表
    if device_list:
        try:
            writer = csv.writer(response)
            writer.writerow(['Device Name', 'iLO IP', 'vCenter', 'DCR', 'CI Type', 'Tier 2', 'Tier 3', 'Status', 'Support Group'])
            for device_info in device_list:
                writer.writerow([device_info['CI_NAME'], device_info['ILO_IP'], device_info['VCENTER'], device_info['DCR'], device_info['CI_TYPE'], device_info['TIER_2'], device_info['TIER_3'], device_info['STATUS_REASON'], device_info['PRIMARY_SUPPORT_GROUP']])
        except Exception as e:
            logger.error('Error writing device info to CSV: ' + str(e))

    return response


def edit_request_pmc_confirm(request):
    try:
        rec = request.POST
        data_center_room = rec.get('dataCenterRoom').upper()
        pmc_id = rec.get('pmcID')
        change_number = rec.get('changeNumber')
        start_time = rec.get('pmcStartTime')
        end_time = rec.get('pmcEndTime')

        device_list_from_mysql = PMCDevicelist.objects.filter(pmc_id=pmc_id)

        device_list = []
        if device_list_from_mysql:
            for device in device_list_from_mysql:
                device_dict = model_to_dict(device)
                renamed_device_dict = {'CI_NAME': device_dict['device_name'], 'CI_TYPE': device_dict['ci_type'],
                                       'STATUS_REASON': device_dict['status'],
                                       'TIER_2': device_dict['tier_2'], 'TIER_3': device_dict['tier_3'],
                                       'PRIMARY_SUPPORT_GROUP': device_dict['support_group'],
                                       'DCR': device_dict['data_center_room'], 'ILO_IP': device_dict['ilo_ip'],
                                       'VCENTER': device_dict['vcenter']}
                device_list.append(renamed_device_dict)
        else:
            device_list = cmdb_request.get_pmc_device_list(data_center_room)

        backup_device_list = []
        for device_dict in device_list:
            # Collect Backup devices
            if 'BCK' in device_dict['CI_NAME'] or 'bck' in device_dict['CI_NAME']:
                backup_device_list.append(device_dict['CI_NAME'])

            # Write device list into pmc_operation table
            if device_dict['CI_TYPE'] == 'Cluster' and device_dict['TIER_2'] == 'Storage':
                PMCOperation.objects.create(pmc_id=pmc_id, pmc_confirmed=1, device_name=device_dict['CI_NAME'], nas_cluster_flag=1)
            elif device_dict['CI_TYPE'] == 'Computer System' and device_dict['TIER_2'] == 'Hardware':
                if 'VMH' in device_dict['CI_NAME']:
                    PMCOperation.objects.create(pmc_id=pmc_id, pmc_confirmed=1, device_name=device_dict['CI_NAME'], ilo_ip=device_dict['ILO_IP'], vcenter_fqdn=device_dict['VCENTER'], esx_flag=1)
                else:
                    PMCOperation.objects.create(pmc_id=pmc_id, pmc_confirmed=1, device_name=device_dict['CI_NAME'], ilo_ip=device_dict['ILO_IP'])
            else:
                continue
        
        # Schedule Backup devices downtime via SSP3 API
        if backup_device_list:
            backup_access_token = backup_request.backup_login()

            # Get the PMC activity via pmc_id
            pmc_activity = PMCActivities.objects.get(pmc_id=pmc_id)
            for backup_device in backup_device_list:
                # Get the schedule id via random int
                schedule_id = str(random.randint(1000, 9999))

                # Convert the timezone to CET
                cet = pytz.timezone('CET')
                start_time_cet = cet.localize(datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
                end_time_cet = cet.localize(datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S'))

                # Schedule backup downtime via API
                if not backup_request.backup_downtime_schedule(backup_access_token, schedule_id, change_number, backup_device, start_time_cet.strftime('%Y-%m-%d %H:%M:%S.%f'), end_time_cet.strftime('%Y-%m-%d %H:%M:%S.%f')):
                    return JsonResponse({'status': False, 'error': 'Error schedule backup downtime, please contact administrator.'})

                # Save the Backup downtime schedule into MySQL
                PMCBackupschedule.objects.create(schedule_id=schedule_id, change_number=pmc_activity.change_number, backup_device_name=backup_device, start_time=int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))), end_time=int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))), pmc_activity=pmc_activity)
        else:
            logger.info('No Backup deivce in this PMC, skipping schedule backup downtime.')
        
    except Exception as e:
        logger.error('Error confirming PMC activity: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True})


def edit_request_view_device_list(request):
    try:
        rec = request.POST
        pmc_id = rec.get('pmc_id')
        data_center_room = rec.get('data_center_room').upper()
        device_list = []

        device_list_from_mysql = PMCDevicelist.objects.filter(pmc_id=pmc_id)

        if device_list_from_mysql:
            for device in device_list_from_mysql:
                device_dict = model_to_dict(device)
                renamed_device_dict = {'CI_NAME': device_dict['device_name'], 'CI_TYPE': device_dict['ci_type'], 'STATUS_REASON': device_dict['status'],
                                       'TIER_2': device_dict['tier_2'], 'TIER_3': device_dict['tier_3'], 'PRIMARY_SUPPORT_GROUP': device_dict['support_group'],
                                       'DCR': device_dict['data_center_room'], 'ILO_IP': device_dict['ilo_ip'], 'VCENTER': device_dict['vcenter']}
                device_list.append(renamed_device_dict)
        else:
            device_list = cmdb_request.get_pmc_device_list(data_center_room)

    except Exception as e:
        logger.error('Error getting device list data: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True, 'device_list': device_list})


def edit_request_save_device_list(request):

    try:
        rec = request.POST
        if request.session.get('user_account')['guest_account'] == 1:
            return JsonResponse({'status': False, 'error': 'You don\'t have permission to edit device list.'})

        pmc_id = rec.get('pmc_id')
        device_list = json.loads(rec.get('device_list'))

        device_list_is_exist = PMCDevicelist.objects.filter(pmc_id=pmc_id)

        if device_list_is_exist:
            PMCDevicelist.objects.filter(pmc_id=pmc_id).delete()

        for device in device_list:
            if not all(value is None or value == '' for value in device.values()):
                PMCDevicelist.objects.create(
                    pmc_id=pmc_id,
                    device_name=device['Device Name'],
                    ilo_ip=device['iLO IP'],
                    vcenter=device['vCenter'],
                    data_center_room=device['DCR'],
                    ci_type=device['CI Type'],
                    tier_2=device['Tier 2'],
                    tier_3=device['Tier 3'],
                    status=device['Status'],
                    support_group=device['Support Group']
                )
            else:
                continue
    except Exception as e:
        logger.error('Error saving device list to MySQL: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True})
