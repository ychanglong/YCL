# -*- coding: utf-8 -*-
# @Time        : 2023/03/01
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Monitoring
# @Project     : GOC Automation Platform

from resource_base.modules.importModules import *
from monitoringweb.scripts import netiq_request, icinga_request
from mainweb.models import TimeSavingStatistics
from django.core.cache import caches
import arrow
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


def maintenance_index(request):
    """Return maintenance page
        Args:
            request
        Returns:
            Render to maintenance_mode.html
    """
    return render(request, 'monitoring/maintenance_mode.html')


def maintenance_execute(request):
    """Maintenance mode
    Args:
        request:
            initiator: User ID who take the action
            maintenance_action: action type
            datetime_start: start maintenance time
            datetime_end: end maintenance time
            comment: maintenance comment
            host_list: maintenance host list
    Returns:
        JsonResponse:
            status: execute result
            success_servers: successful servers
            failed_servers: failed servers
    """
    # Get the request data
    rec = request.POST

    initiator = request.session.get('user_account')['loginid']
    maintenance_action = rec.get('maintenanceAction')
    datetime_start = rec.get('dateTimeFrom')
    datetime_end = rec.get('dateTimeTo')
    comment = rec.get('comment')
    host_list = rec.get('hostList').split(',')
    user_timezone = request.session['user_account']['timezone']

    # Restrict the number of hosts within 200
    if len(host_list) > 200:
        return JsonResponse({'status': False, 'error': 'Please limit the number of hosts within 200!'})

    # Logging the request details
    if maintenance_action == '1':
        logger.info(request.session['user_account']['loginid'] + ' is setting maintenance mode for %s' % (str(host_list)))
        logger.info('User timezone: ' + user_timezone)
        logger.info('Time frame: %s to %s , Comment: %s' % (str(datetime_start), str(datetime_end), comment))
    elif maintenance_action == '2':
        logger.info(request.session['user_account']['loginid'] + ' is exiting maintenance mode for %s' % (str(host_list)))

    # Define response list
    success_servers = []
    failed_servers = []

    try:
        # Category Windows and linux servers
        cache = caches['default']
        icinga_host_list = []
        netiq_host_list = []
        for host in host_list:
            host_os_type = cache.get(host + "_os_type")

            if host_os_type == 'unix server':
                host_dns_domain = cache.get(host + "_dns_domain")
                icinga_host_list.append(host + '.' + host_dns_domain)
            elif host_os_type == 'windows server':
                netiq_host_list.append(host)
            else:
                logger.info('Skip host due to OS type not in (Unix, Windows): ' + host)
                continue

        # Define response dict
        icinga_res_dict = {}
        netiq_res_dict = {}

        # Convert the start&end time zone to Asia/Shanghai
        datetime_start_arrow = arrow.get(datetime_start, "YYYY-MM-DD HH:mm:ss", tzinfo=user_timezone)
        datetime_end_arrow = arrow.get(datetime_end, "YYYY-MM-DD HH:mm:ss", tzinfo=user_timezone)

        # maintenance_action: 1 - StartMaintenanceMode, 2 - StopMaintenanceMode
        # Action is start maintenance for servers
        if maintenance_action == '1':
            if icinga_host_list:
                # Call ICINGA2 maintenance API
                logger.info('Calling ICINGA2 Schedule Downtime API')
                icinga_res_dict = icinga_request.schedule_downtime(icinga_host_list, datetime_start_arrow.timestamp(), datetime_end_arrow.timestamp(), initiator=initiator, comment=comment)
            if netiq_host_list:
                # Call NetIQ maintenance API
                logger.info('Calling NETIQ Start Maintenance Mode API')
                netiq_res_dict = netiq_request.maintenance_mode(netiq_host_list, 'StartMaintenanceMode', initiator=initiator)

            # Response code: 200 indicates successfully ended
            for server, result in merge(icinga_res_dict, netiq_res_dict).items():
                if '.' in server:
                    server = server.split('.')[0]

                # Response None indicates failed ended
                if result is None or result != 200:
                    # Collect failed server list
                    failed_servers.append(server)
                else:
                    # Collect successful server list
                    success_servers.append(server)

        # Action is stop maintenance for servers
        elif maintenance_action == '2':
            if icinga_host_list:
                # Call ICINGA2 maintenance API
                logger.info('Calling ICINGA2 Remove Downtime API')
                icinga_res_dict = icinga_request.remove_downtime(icinga_host_list)
            if netiq_host_list:
                # Call NetIQ maintenance API
                logger.info('Calling NETIQ Stop Maintenance Mode API')
                netiq_res_dict = netiq_request.maintenance_mode(netiq_host_list, 'StopMaintenanceMode', initiator=initiator)

            # Response code: 200 indicates successfully ended
            for server, result in merge(icinga_res_dict, netiq_res_dict).items():
                if '.' in server:
                    server = server.split('.')[0]

                # Response None indicates failed ended
                if result is None or result != 200:
                    # Collect failed server list
                    failed_servers.append(server)
                else:
                    # Collect successful server list
                    success_servers.append(server)

        else:
            # No accept action received, return error
            logger.warning('Warning: The maintenance action is not in scope')
            return JsonResponse({'status': False, 'error': 'The maintenance action is not in scope'})
    except Exception as e:
        logger.error('Error setting maintenance mode: %s' % (str(e),))
        return JsonResponse({'status': False, 'error': 'Unknown Exception:' + str(e)})

    # Time saving statistic
    TimeSavingStatistics.time_saving_statistic('maintenance_mode', len(success_servers) * 300)
    logger.info('The maintenance action completed successfully, success_servers: %s failed_servers: %s' % (str(success_servers), str(failed_servers)))
    return JsonResponse({'status': True, 'total': len(success_servers) + len(failed_servers), 'data': {'success_servers': success_servers, 'failed_servers': failed_servers}})
