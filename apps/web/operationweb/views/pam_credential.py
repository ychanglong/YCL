# -*- coding: utf-8 -*-
# @Time        : 2023/03/01
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Operation Tools
# @Project     : GOC Automation Platform

from resource_base.modules.importModules import *
import logging
from operationweb.scripts import pam_request
from mainweb.models import TimeSavingStatistics

# Get the django logger
logger = logging.getLogger('django')


def pam_credential_index(request):
    return render(request, 'operation/pam_credential.html')


def pam_credential_search(request):
    try:
        # Get the request data
        rec = request.POST
        account_type = rec.get('accountType')
        nt_password = rec.get('ntPassword')
        comment = rec.get('comment')
        host_list = rec.get('hostList').lower().split(',')
        loginid = request.session['user_account']['loginid']

        # Restrict the number of hosts within 200
        if len(host_list) > 200:
            return JsonResponse({'status': False, 'error': 'Please limit the number of hosts within 200!'})

        logger.info(loginid + ' is searching PAM credentials for ' + str(host_list))

        pam_credentials_list = pam_request.get_pam_credential(loginid, nt_password, account_type, host_list, comment)

    except Exception as e:
        logger.error('Error getting PAM credential: ' + str(e))
        return JsonResponse({'status': False})

    if pam_credentials_list:
        # Time saving statistic
        credential_host_list = []
        for credential_dict in pam_credentials_list:
            credential_host_list.append(credential_dict['host_name'])

        TimeSavingStatistics.time_saving_statistic('pam_credential', len(list(set(credential_host_list))) * 300)
        return JsonResponse({'status': True, 'data': pam_credentials_list})
    else:
        return JsonResponse({'status': False, 'error': 'PAM API connection issue, please try again later...'})
