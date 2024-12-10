# -*- coding: utf-8 -*-
# @Time        : 2024/09/05
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Operation Tools
# @Project     : GOC Automation Platform

import logging
from resource_base.modules.importModules import *
from operationweb.scripts import win_hotfix_check
from mainweb.models import TimeSavingStatistics
from django.views.decorators.csrf import csrf_exempt

# Get the django logger
logger = logging.getLogger('django')


def win_hotfix_check_index(request):
    return render(request, 'operation/win_hotfix_check.html')


def win_hotfix_check_execute(request):
    try:
        # Get the request data
        rec = request.POST
        loginid = request.session['user_account']['loginid']
        nt_password = rec.get('ntPassword')
        host_list = rec.get('hostList').strip().split(',')

        logger.info(request.session.get('user_account')['loginid'] + ' is checking host up time for: %s' % (
        str(host_list),))

        up_time_list_result = win_hotfix_check.get_server_uptime_and_hotfix(host_list, loginid, nt_password, '1')

        logger.info('Uptime check result: ' + str(up_time_list_result))

    except Exception as e:
        logger.error('Error checking disk utilization: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    # Time saving statistic
    TimeSavingStatistics.time_saving_statistic('win_hotfix_check', 390)
    return JsonResponse({'status': True, 'data': up_time_list_result})


@csrf_exempt
def win_hotfix_list_execute(request):
    try:
        # Get the request data
        rec = request.POST
        loginid = request.session['user_account']['loginid']
        nt_password = rec.get('ntPassword')
        host_name = rec.get('hostName').lower()

        logger.info(request.session.get('user_account')['loginid'] + ' is checking host hotfix list for: %s' % (
        str(host_name),))

        hostfix_list_result = win_hotfix_check.get_server_uptime_and_hotfix([host_name,], loginid, nt_password, '2')

        logger.info('Hotfix list check result: ' + str(hostfix_list_result))

    except Exception as e:
        logger.error('Error checking disk utilization: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    # Time saving statistic
    TimeSavingStatistics.time_saving_statistic('win_hotfix_check', 390)
    return JsonResponse({'status': True, 'data': hostfix_list_result})
