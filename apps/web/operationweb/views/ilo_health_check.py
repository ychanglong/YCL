# -*- coding: utf-8 -*-
# @Time        : 2023/08/02
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Operation Tools
# @Project     : GOC Automation Platform

import requests
import logging
from resource_base.modules.importModules import *
from operationweb.scripts import pam_request
from django.views.decorators.csrf import csrf_exempt
from mainweb.models import TimeSavingStatistics

# Get the django logger
logger = logging.getLogger('django')


def ilo_health_check_index(request):
    return render(request, 'operation/ilo_health_check.html')


def ilo_health_check_execute(request):
    try:
        # Get the request data
        rec = request.POST
        account_type = "1"
        loginid = request.session['user_account']['loginid']
        nt_password = rec.get('ntPassword')
        comment = rec.get('comment')
        ilo_host_list = rec.get('hostList').split(',')
        logger.info(loginid + ' is checking health for ' + str(ilo_host_list))

        # 构造POST请求数据
        body = {
            'host_list': rec.get('hostList').split(','),
            'pam_credentials_list': pam_request.get_pam_credential(loginid, nt_password,
                                                                   account_type, ilo_host_list, comment)
        }

        response = requests.post('http://10.187.51.133:5000/ilo_health_check_execute', json=body)
        response.raise_for_status()     # Raises a HTTPError if the response status is 4xx, 5xx
        server_info = response.json()
        server_info_list = server_info['data']
        return JsonResponse({'status': True, 'data': server_info_list})

        # return JsonResponse({'status': True, 'data': response.json()})
        # return JsonResponse(response.json(), status=response.status_code)

    except requests.exceptions.HTTPError as err:
        logger.error('HTTP Error:', err)
        return JsonResponse({'status': False, 'error': 'HTTP Error: ' + str(err)}, status=500)
    except Exception as e:
        logger.error('Error getting iLO status: ' + str(e))
        return JsonResponse({'status': False, 'error': 'Error getting iLO status: ' + str(e)}, status=500)


@csrf_exempt
def ilo_health_detail(request):
    try:
        # Get the request data
        rec = request.POST
        account_type = "1"
        loginid = request.session['user_account']['loginid']
        nt_password = rec.get('ntPassword')
        comment = rec.get('comment')
        host_name = rec.get('host_name')
        url = host_name + "r.rb-obm.bosch-org.com"

        # 构造POST请求数据
        body = {
            'url': url,
            'pam_credentials_list': pam_request.get_pam_credential(loginid, nt_password, account_type,
                                                                                    [host_name], comment)
        }

        response = requests.post('http://10.187.51.133:5000/get_health_data', json=body)
        response.raise_for_status()
        health_data = response.json()['data']
        logger.info(health_data)

        # Time saving statistic
        TimeSavingStatistics.time_saving_statistic('ilo_health_check', 270)

    except Exception as e:
        logger.error('Error getting iLO status: ' + str(e))
        return JsonResponse({'status': False})

    return JsonResponse({'status': True, 'data': health_data})

# @csrf_exempt
# def ilo_health_detail(request):
#     try:
#         rec = request.POST
#         account_type = "1"
#         loginid = request.session['user_account']['loginid']
#         nt_password = rec.get('ntPassword')
#         comment = rec.get('comment')
#         host_name = rec.get('host_name')
#         url = host_name + "r.rb-obm.bosch-org.com"
#         # get pam account & password via get_pam_credential method.
#         pam_credentials_list = pam_request.get_pam_credential(loginid, nt_password, account_type, [host_name], comment)
#         # get health data via get_embedded_health
#         health_data = ilo_request.get_health_data(pam_credentials_list, url)
#
#         # Time saving statistic
#         TimeSavingStatistics.time_saving_statistic('ilo_health_check', 270)
#
#     except Exception as e:
#         logger.error('Error getting iLO status: ' + str(e))
#         return JsonResponse({'status': False})
#
#     return JsonResponse({'status': True, 'data': health_data})


@csrf_exempt
def ilo_get_ahs(request):
    try:
        rec = request.POST
        account_type = "1"
        loginid = request.session['user_account']['loginid']
        nt_password = rec.get('ntPassword')
        comment = rec.get('comment')
        host_name = rec.get('host_name').lower()
        url = host_name + "r.rb-obm.bosch-org.com"

        # 构造POST请求数据
        body = {
            'host_name': host_name,
            'url': url,
            'pam_credentials_list': pam_request.get_pam_credential(loginid, nt_password, account_type,
                                                                   [host_name], comment)
        }

        response = requests.post('http://10.187.51.133:5000/get_ahs_log', json=body)

        # response = ilo_request.get_ahs_log(pam_credentials_list, url, host_name)

        # Time saving statistic
        TimeSavingStatistics.time_saving_statistic('ilo_get_ahs', 270)

        if response:
            # Create a HttpResponse object with the appropriate headers for file download
            response = HttpResponse(response.content, content_type='application/octet-stream')
            return response
        else:
            JsonResponse({'error': 'AHS log not found.'}, status=500)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def ilo_reset_ilo(request):
    try:
        # Get the request data
        rec = request.POST
        account_type = "1"
        loginid = request.session['user_account']['loginid']
        nt_password = rec.get('ntPassword')
        comment = rec.get('comment')
        host_name = rec.get('host_name')
        url = host_name + "r.rb-obm.bosch-org.com"

        # 构造POST请求数据
        body = {
            'url': url,
            'pam_credentials_list': pam_request.get_pam_credential(loginid, nt_password, account_type,
                                                                   [host_name], comment)
        }

        requests.post('http://10.187.51.133:5000/reset_ilo', json=body)

        TimeSavingStatistics.time_saving_statistic('ilo_get_ahs', 270)

    except Exception as e:
        logger.error(f'Error resetting iLO: {e}')
        return JsonResponse({'status': False, 'error': str(e)}), 500

    return JsonResponse({'status': True, 'message': 'iLO reset successfully'})


@csrf_exempt
def ilo_get_iml(request):
    try:
        rec = request.POST
        account_type = "1"
        loginid = request.session['user_account']['loginid']
        nt_password = rec.get('ntPassword')
        comment = rec.get('comment')
        host_name = rec.get('host_name').lower()
        url = host_name + "r.rb-obm.bosch-org.com"

        # 构造POST请求数据
        body = {
            'host_name': host_name,
            'url': url,
            'pam_credentials_list': pam_request.get_pam_credential(loginid, nt_password, account_type,
                                                                   [host_name], comment)
        }

        response = requests.post('http://10.187.51.133:5000/get_iml_log', json=body)

        # response = ilo_request.get_ahs_log(pam_credentials_list, url, host_name)

        # Time saving statistic
        TimeSavingStatistics.time_saving_statistic('ilo_get_iml', 270)

        if response:
            # Create a HttpResponse object with the appropriate headers for file download
            response = HttpResponse(response.content, content_type='application/octet-stream')
            return response
        else:
            JsonResponse({'error': 'IML log not found.'}, status=500)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
