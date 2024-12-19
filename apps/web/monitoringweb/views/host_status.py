# -*- coding: utf-8 -*-
# @Time        : 2023/03/01
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Monitoring
# @Project     : GOC Automation Platform

from resource_base.modules.importModules import *
from monitoringweb.scripts import icinga_request
from monitoringweb.models import HostInfo
from mainweb.models import TimeSavingStatistics
from django.core.cache import caches
from django.views.decorators.csrf import csrf_exempt
import logging

# Get the django logger
logger = logging.getLogger('django')


def host_status_index(request):
    """Redirect host status page
            Args:
                request
            Returns:
                Render to host_status.html
    """
    return render(request, 'monitoring/host_status.html')


def host_search(request):
    """Host search
    Args:
        request:
            host_name: User input host name
    Returns:
        JsonResponse:
            search_result: All hosts list which matches the user input host name
    """
    rec = request.POST
    host_name = rec.get('hostName')
    # Define return list
    search_result = []

    try:
        if host_name:
            # Use CACHES default settings in settings.py
            cache = caches['default']

            # Query the hosts from Redis
            c_host_list = cache.get_many(cache.keys(host_name.lower() + "*_dns_domain"))

            # Save the search result
            for host in c_host_list.items():
                search_result.append(host[0].split('_')[0])

            logger.info('Host search result: ' + str(search_result))
    except Exception as e:
        logger.error('Error searching the host name from Redis: %s' % (str(e),))
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True, 'data': {'result': search_result}})


@csrf_exempt
def host_status_search(request):
    """Host status search
    Args:
        request:
            host_list: User input host name list
    Returns:
        JsonResponse:
            search_result: All hosts status for the host list
    """
    # Get the request data
    rec = request.POST
    host_list = rec.get('hostList').split(',')

    # Restrict the number of hosts within 200
    if len(host_list) > 200:
        return JsonResponse({'status': False, 'error': 'Please limit the number of hosts within 200!'})

    logger.info(request.session['user_account']['loginid'] + ' is searching host status for: %s' % (str(host_list),))

    # Return data list
    host_status_all = []

    try:
        # Currently Linux only, delete Windows hosts (SRE Linux pilot)
        cache = caches['default']
        icinga_host_list = []
        for host in host_list:
            host_os_type = cache.get(host + "_os_type")

            if host_os_type == 'unix server':
                host_dns_domain = cache.get(host + "_dns_domain")
                icinga_host_list.append(host + '.' + host_dns_domain)
        # Currently Linux only, delete Windows hosts (SRE Linux pilot)

        if icinga_host_list:
            host_status_all = list(icinga_request.host_status_search(icinga_host_list).values())

    except Exception as e:
        logger.error('Error searching the host status: %s' % (str(e),))

    if host_status_all:
        # Time saving statistic
        TimeSavingStatistics.time_saving_statistic('host_status', len(host_status_all) * 170)
        return JsonResponse({'status': True, 'data': host_status_all})
    else:
        return JsonResponse({'status': False, 'error': 'No data found for provided hosts.'})
