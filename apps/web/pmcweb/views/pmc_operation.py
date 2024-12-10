# -*- coding: utf-8 -*-
# @Time        : 2023/08/02
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : PMC
# @Project     : GOC Automation Platform

from resource_base.modules.importModules import *
from pmcweb.models import PMCActivities, PMCOperation, PMCAssignee
from pmcweb.scripts import pmc_request
import asyncio
import logging
import re
from redis import Redis

# Get the django logger
logger = logging.getLogger('django')


def pmc_operation_index(request):
    """Return pmc operation page
        Args:
            request
        Returns:
            Render to pmc_operation.html
    """
    return render(request, 'pmc/pmc_operation.html')


def pmc_operation_search_activity(request):
    confirmed_pmc_list = []
    try:
        rec = request.POST
        change_number = rec.get('searchChangeNumber')
        location_code = rec.get('searchLocationCode')

        if not change_number and not location_code:
            pmc_activities = list(PMCActivities.objects.filter(Q(data_status=1) & Q(status__in=[0, 1, 2, 3])).values())
        else:
            pmc_activities = list(PMCActivities.objects.filter(Q(change_number=change_number) | Q(location_code=location_code), (Q(data_status=1) & Q(status__in=[0, 1, 2, 3]))).values())

        for pmc_activity in pmc_activities:
            pmc_activity_confirmed = PMCOperation.objects.filter(pmc_id=pmc_activity['pmc_id'])
            if pmc_activity_confirmed:
                activity_temp = {'pmc_id': pmc_activity['pmc_id'],
                                 'change_number': pmc_activity['change_number'],
                                 'region': pmc_activity['region'],
                                 'location_code': pmc_activity['location_code'],
                                 'data_center_room': pmc_activity['data_center_room'],
                                 'start_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pmc_activity['start_time'])) if pmc_activity['start_time'] else '-',
                                 'end_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pmc_activity['end_time'])) if pmc_activity['end_time'] else '-',
                }
                confirmed_pmc_list.append(activity_temp)

        logger.info('Confirmed PMC activity list: ' + str(confirmed_pmc_list))

    except Exception as e:
        logger.error('Error searching confirmed PMC activity: ' + str(e))

    return JsonResponse({'status': True, 'data': confirmed_pmc_list})


def pmc_operation_execute(request):
    try:
        rec = request.POST
        pmc_id = rec.get('pmc_id')
        execution_mode = rec.get('mode')
        nt_account = request.session.get('user_account')['loginid']
        rbadmin_account = 'rb-admin\\' + request.session.get("user_account")["loginid"] + '_rba'
        nt_password = rec.get('nt_password')
        rbadmin_password = rec.get('rbadmin_password')
        pmc_operation_device_list = list(PMCOperation.objects.filter(pmc_id=pmc_id).values())

        logger.info(nt_account + ' executed for PMC activity: ' + str(pmc_id))
        logger.info('PMC device list: ' + str(pmc_operation_device_list))

        ESX_dict = {}
        NOESX_dict = {}
        vcenter_list = []
        storage_list = []

        for device in pmc_operation_device_list:
            if device['esx_flag'] == 1:
                ESX_dict[device['device_name']] = device['ilo_ip']
                vcenter_list.append(device['vcenter_fqdn'])
            else:
                if device['nas_cluster_flag'] == 1:
                    storage_list.append(device['device_name'])
                else:
                    NOESX_dict[device['device_name']] = device['ilo_ip']

        if len(ESX_dict) + len(NOESX_dict) >= 60:
            logger.error('The number of hardware machines cannot exceed 60.')
            return JsonResponse({'status': False, 'error': 'The number of hardware machines cannot exceed 60.'})

        pmc_activity = PMCActivities.objects.get(pmc_id=pmc_id)

        # Restrict execute user
        if execution_mode == 'poweron':
            pattern = r"\([^)]*\)"
            power_on_assignee_name = re.sub(pattern, "", pmc_activity.power_on_assignee).strip()
            power_on_assignee = PMCAssignee.objects.filter(assignee_name=power_on_assignee_name).values()[0]
            if power_on_assignee['assignee_nt'].lower() != nt_account.lower():
                return JsonResponse({'status': False, 'error': 'You dont have permission to perform this action.'})
        elif execution_mode == 'poweroff':
            pattern = r"\([^)]*\)"
            power_off_assignee_name = re.sub(pattern, "", pmc_activity.power_off_assignee).strip()
            power_off_assignee = PMCAssignee.objects.filter(assignee_name=power_off_assignee_name).values()[0]
            if power_off_assignee['assignee_nt'].lower() != nt_account.lower():
                return JsonResponse({'status': False, 'error': 'You dont have permission to perform this action.'})

        request_body = {
            "ESX": ESX_dict,
            "NoESX": NOESX_dict,
            "storages": storage_list,
            "ntAccount": nt_account,
            "ntPass": nt_password,
            "vcenterAccount": rbadmin_account,
            "vcenterPass": rbadmin_password,
            "vcenter": vcenter_list,
            "CRQ": pmc_activity.change_number
        }

        # Non-blocking asynchronously send power on request
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        if execution_mode == 'poweron':
            loop.run_in_executor(None, pmc_request.power_on, request_body)
        elif execution_mode == 'poweroff':
            loop.run_in_executor(None, pmc_request.power_off, request_body)
        else:
            return JsonResponse({'status': False, 'error': 'Unknow execution mode.'})

    except Exception as e:
        logger.error('Error occurred during power on request: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True})


def pmc_operation_execution_log(request):
    try:
        rec = request.POST
        pmc_id = rec.get('pmc_id')

        # Use CACHES pmc settings in settings.py
        pmc_cache = Redis(host='10.8.136.243', port=6379, db=1, password='Abcd@1234')

        change_number = PMCActivities.objects.get(pmc_id=pmc_id).change_number

        poweron_log = [byte.decode() for byte in pmc_cache.lrange(change_number + '_poweronlog', 0, -1)]
        poweroff_log = [byte.decode() for byte in pmc_cache.lrange(change_number + '_powerofflog', 0, -1)]

        pmc_operation_logs = {'poweron_log': poweron_log, 'poweroff_log': poweroff_log}
        return JsonResponse({'status': True, 'pmc_operation_logs': pmc_operation_logs})

    except Exception as e:
        logger.error('Error retrieving PMC operation log: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})
