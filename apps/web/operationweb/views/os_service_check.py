# -*- coding: utf-8 -*-
# @Time        : 2023/12/27
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Operation Tools
# @Project     : GOC Automation Platform

import logging
from resource_base.modules.importModules import *
from operationweb.scripts import os_service_check

# Get the django logger
logger = logging.getLogger('django')


def os_service_check_index(request):
    return render(request, 'operation/os_service_check.html')


def os_service_check_execute(request):
    rec = request.POST
    loginid = request.session['user_account']['loginid']
    host_name = rec.get('hostName')
    nt_password = rec.get('ntPassword')
    service_name = rec.get('serviceName')
    operation_tag = rec.get('operationTag')

    if operation_tag == '1':
        logger.info(loginid + ' is checking service ' + service_name + ' for ' + host_name)
    else:
        logger.info(loginid + ' is restarting service ' + service_name + ' for ' + host_name)

    result = os_service_check.windows_service_check(host_name, loginid, nt_password, service_name, operation_tag)

    logger.info('Service status info: ' + str(result))

    return JsonResponse({'status': True, 'data': result})

