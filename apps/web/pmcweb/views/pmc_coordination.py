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
import arrow
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
        user_timezone = request.session.get('user_account')['timezone']

        pmc_activity = model_to_dict(PMCActivities.objects.get(pmc_id=rec.get('pmc_id')))
        pmc_confirmed = PMCOperation.objects.filter(pmc_id=rec.get('pmc_id'))
        if pmc_confirmed:
            pmc_activity['pmc_confirmed'] = '1'
        else:
            pmc_activity['pmc_confirmed'] = '0'

        pmc_activity['start_time'] = arrow.get(pmc_activity['start_time']).to(user_timezone).format('YYYY-MM-DD HH:mm:ss') if pmc_activity['start_time'] else ''
        pmc_activity['end_time'] = arrow.get(pmc_activity['end_time']).to(user_timezone).format('YYYY-MM-DD HH:mm:ss') if pmc_activity['end_time'] else ''

        pmc_activity_plan = list(PMCActivityplan.objects.filter(pmc_id=rec.get('pmc_id')).values())


    except Exception as e:
        logger.error('Error retrieving PMC activity: ' + str(e))

    return render(request, 'pmc/pmc_edit_request.html', {'pmc_activity': json.dumps(pmc_activity), 'pmc_activity_plan': json.dumps(pmc_activity_plan)})


def pmc_public_view_index(request):
    """Return pmc public view page
        Args:
            request
        Returns:
            Render to pmc_public_view.html
    """
    return render(request, 'pmc/pmc_public_view.html')


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
        san_assignee_list_str = ''
        user_timezone = request.session.get('user_account')['timezone']

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
            for san_assignee in rec.getlist('sanAssignee'):
                san_assignee_list_str += (san_assignee + ';')
            san_assignee_list_str = san_assignee_list_str[:-1]

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
        pmc_start_time = arrow.get(rec.get('pmcStartTime'), "YYYY-MM-DD HH:mm:ss", tzinfo=user_timezone).timestamp()
        pmc_end_time = arrow.get(rec.get('pmcEndTime'), "YYYY-MM-DD HH:mm:ss", tzinfo=user_timezone).timestamp()

        pmc_activity = PMCActivities(
            itsp_no=rec.get('itspNumber'),
            data_status=1,
            data_center_room=rec.get('dataCenterRoom'),
            change_class=rec.get('changeClass'),
            reason=rec.get('reason'),
            start_time=pmc_start_time,
            end_time=pmc_end_time,
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
            pmc_coordinator=rec.get('pmcCoordinator'),
            san_assignee = san_assignee_list_str
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
        user_timezone = request.session.get('user_account')['timezone']
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
                             'start_time': arrow.get(activity['start_time']).to(user_timezone).format('YYYY-MM-DD HH:mm:ss') if activity['start_time'] else '-',
                             'end_time': arrow.get(activity['end_time']).to(user_timezone).format('YYYY-MM-DD HH:mm:ss') if activity['end_time'] else '-',
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
        user_timezone = request.session.get('user_account')['timezone']

        pmc_activity['start_time'] = arrow.get(pmc_activity['start_time']).to(user_timezone).format('YYYY-MM-DD HH:mm:ss') if pmc_activity['start_time'] else ''
        pmc_activity['end_time'] = arrow.get(pmc_activity['end_time']).to(user_timezone).format('YYYY-MM-DD HH:mm:ss') if pmc_activity['end_time'] else ''

    except Exception as e:
        logger.error('Error retrieving PMC activity: ' + str(e))
        return JsonResponse({'status': False, 'error': 'Error retrieving PMC activity: ' + str(e)})

    return JsonResponse({'status': True, 'data': pmc_activity})


def edit_request_save_activity(request):
    try:
        rec = request.POST
        user_timezone = request.session.get('user_account')['timezone']

        if request.session.get('user_account')['guest_account'] == 1:
            return JsonResponse({'status': False, 'error': 'You don\'t have permission to edit PMC requests.'})

        # Save to PMC Activity
        pmc_activity = PMCActivities.objects.get(pmc_id=rec.get('pmcID'))

        # Keep previous pmc status
        previous_pmc_status = pmc_activity.status

        pmc_activity.data_center_room = rec.get('dataCenterRoom')
        pmc_activity.change_class = rec.get('changeClass')
        pmc_activity.start_time = arrow.get(rec.get('pmcStartTime'), "YYYY-MM-DD HH:mm:ss", tzinfo=user_timezone).timestamp()
        pmc_activity.end_time = arrow.get(rec.get('pmcEndTime'), "YYYY-MM-DD HH:mm:ss", tzinfo=user_timezone).timestamp()
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

        # Save SAN and SAN assignee selection
        san_assignee_list_str = ''

        if 'TOBECHECKED' in rec.getlist('sanSelection'):
            pmc_activity.san_vnx = 2
            pmc_activity.san_unity = 2
            pmc_activity.san_vplex = 2
        elif 'NO' in rec.getlist('sanSelection'):
            pmc_activity.san_vnx = 0
            pmc_activity.san_unity = 0
            pmc_activity.san_vplex = 0
        else:
            for san_assignee in rec.getlist('sanAssignee'):
                san_assignee_list_str += (san_assignee + ';')
            san_assignee_list_str = san_assignee_list_str[:-1]

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
        
        pmc_activity.san_assignee = san_assignee_list_str

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
                                               start_time=plan_data['Start time <span style="color: red;">(UTC+0)</span>'],
                                               description_of_activity=plan_data['Description of the activities'],
                                               execution=plan_data['Execution'],
                                               responsible=plan_data['Responsible Team/Person'],
                                               information_to=plan_data['Give Information To']
                                               )
            data_to_be_saved.save()
        
        # Send PMC close notification to backup team
        schedule_close_result = True
        if rec.get('pmcStatus') == '4' and previous_pmc_status != 4:
            backup_schedule = PMCBackupschedule.objects.filter(pmc_activity_id=pmc_activity.pmc_id)[0]
            backup_access_token = backup_request.backup_login()
            schedule_close_result = backup_request.backup_schedule_close(backup_access_token, backup_schedule.schedule_id, backup_schedule.change_number)

            if schedule_close_result:
                # Backup schedule close request successful, update the schedule status to completed
                backup_schedule.schedule_status = 2
                backup_schedule.save()
                return JsonResponse({'status': True, 'msg': 'All save operations successfully.'})
            else:
                return JsonResponse({'status': True, 'msg': 'PMC activity saved, backup schedule close request failed.'})

    except Exception as e:
        logger.error('Error saving PMC activity: ' + str(e))
        return JsonResponse({'status': False, 'error': 'Error saving PMC activity: ' + str(e)})

    return JsonResponse({'status': True, 'msg': 'All save operations successfully.'})


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
        user_timezone = request.session.get('user_account')['timezone']

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
            schedule_result = False
            schedule_result_list = []
            backup_device_list_str = ''

            # Convert the timezone to CET
            start_time_arrow = arrow.get(start_time, "YYYY-MM-DD HH:mm:ss", tzinfo=user_timezone)
            end_time_arrow = arrow.get(end_time, "YYYY-MM-DD HH:mm:ss", tzinfo=user_timezone)
            start_time_cet = start_time_arrow.to('Europe/Berlin')
            end_time_cet = end_time_arrow.to('Europe/Berlin')
            
            backup_access_token = backup_request.backup_login()

            # Get the PMC activity via pmc_id
            pmc_activity = PMCActivities.objects.get(pmc_id=pmc_id)

            # Get the schedule id via random int
            random_int = str(pmc_id) + str(random.randint(10, 99))
            schedule_id = random_int if len(random_int) <=4 else random_int[:4]

            for backup_device in backup_device_list:
                # Schedule backup downtime via API
                schedule_result = backup_request.backup_downtime_schedule(backup_access_token, schedule_id, change_number, backup_device, start_time_cet.strftime('%Y-%m-%d %H:%M:%S.%f'), end_time_cet.strftime('%Y-%m-%d %H:%M:%S.%f'))

                # Keep the schedule result
                schedule_result_list.append({'backup_device': backup_device, 'schedule_result': schedule_result})
            
            # Append the successful devices and log failed devices
            for schedule_result_dict in schedule_result_list:
                if schedule_result_dict['schedule_result']:
                    backup_device_list_str += (schedule_result_dict['backup_device'] + ';')
                else:
                    logger.info('Backup downtime schedule for ' + schedule_result_dict['backup_device'] + ' was failed.')
            
            if backup_device_list_str:
                # Save the Backup downtime schedule into MySQL
                PMCBackupschedule.objects.create(schedule_id=schedule_id, change_number=pmc_activity.change_number, backup_device_name=backup_device_list_str[:-1], start_time=start_time_arrow.timestamp(), end_time = end_time_arrow.timestamp(), pmc_activity=pmc_activity)
            else:
                return JsonResponse({'status': False, 'error': 'Error scheduling backup downtime, please contact administrator.'})
        else:
            logger.info('No Backup deivce in this PMC, skipping schedule backup downtime.')
            return JsonResponse({'status': True, 'data': schedule_result_list})
        
    except Exception as e:
        logger.error('Error confirming PMC activity: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True, 'data': schedule_result_list})


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


def pmc_public_view_search_activity(request):
    try:
        rec = request.POST

        pmc_activities = list(PMCActivities.objects.filter((Q(status__in=[0,1,2,3])), Q(data_status=1)).values())

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
                             'start_time': arrow.get(activity['start_time']).to('UTC').format('YYYY-MM-DD HH:mm:ss') if activity['start_time'] else '-',
                             'end_time': arrow.get(activity['end_time']).to('UTC').format('YYYY-MM-DD HH:mm:ss') if activity['end_time'] else '-',
                             'start_with_shutdown': activity['start_with_shutdown'],
                             'change_class': change_class,
                             'pmc_coordinator': activity['pmc_coordinator'],
                             }

            sorted_pmc_activities.append(activity_temp)
            sorted_pmc_activities.sort(key=itemgetter('start_time'), reverse=True)

    except Exception as e:
        logger.error('Error searching PMC activities: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True, 'data': sorted_pmc_activities})
