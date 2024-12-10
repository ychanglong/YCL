# -*- coding: utf-8 -*-
# @Time        : 2023/03/01
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Operation Tools
# @Project     : GOC Automation Platform

from resource_base.modules.importModules import *
from django.core.cache import caches
from django.views.decorators.csrf import csrf_exempt
from monitoringweb.scripts import netiq_request, icinga_request
import logging

# Get the django logger
logger = logging.getLogger('django')


def merge(dict1, dict2):
    """Merging two dict to one
            Args:
                dict1
                dict2
            Returns:
                Dict after merging
    """
    res = {**dict1, **dict2}
    return res


def host_details_index(request):
    return render(request, 'operation/host_details.html')


@csrf_exempt
def host_details_search(request):
    """Host details search
    Args:
        request:
            host_list: User input host name list
    Returns:
        JsonResponse:
            search_result: All hosts info for the host list
    """
    # Get the request data
    rec = request.POST
    host_list = rec.get('hostList').split(',')

    # Restrict the number of hosts within 200
    if len(host_list) > 200:
        return JsonResponse({'status': False, 'error': 'Please limit the number of hosts within 200!'})

    logger.info(request.session.get('user_account')['loginid'] + ' is searching host details for: %s' % (str(host_list),))

    try:
        # Category Windows and linux servers
        cache = caches['default']
        icinga_host_list = []
        netiq_host_list = []
        for host in host_list:
            host_name = cache.get_many(cache.keys(host.lower() + "*_server_name*"))
            for item in host_name.values():
                key_os_type = cache.keys(item.lower() + "*_os_type*")[0]
                key_monitoring_type = cache.keys(item.lower() + "_monitoring_type*")[0]
                os_type = cache.get(key_os_type)
                monitoring_type = cache.get(key_monitoring_type)

                if os_type == 'UNIX Server' and monitoring_type == '1':
                    icinga_host_list.append(item)
                elif os_type == 'Windows Server' and monitoring_type == '2':
                    netiq_host_list.append(item)

        if not icinga_host_list and not netiq_host_list:
            return JsonResponse({'status': False, 'error': 'No host info found for provided hosts!'})

        # Define hosts info dict
        icinga_host_info = {}
        netiq_host_info = {}
        # Get the server owner info from ICINGA2 or NetIQ API
        if icinga_host_list:
            icinga_host_info = icinga_request.host_details_search(icinga_host_list)
        if netiq_host_list:
            netiq_host_info = netiq_request.host_details_search(netiq_host_list)

        if not icinga_host_info and not netiq_host_info:
            return JsonResponse({'status': False, 'error': 'No host info found for provided hosts!'})

        all_host_info = merge(icinga_host_info, netiq_host_info)

        all_data = list(all_host_info.values())

    except Exception as e:
        logger.error('Error searching host details: ' + str(e))
        return JsonResponse({'status': False, 'error': 'Error searching host details: ' + str(e)})

    return JsonResponse({'status': True, 'data': all_data})
