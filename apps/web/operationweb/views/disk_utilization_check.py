# -*- coding: utf-8 -*-
# @Time        : 2023/08/02
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Operation Tools
# @Project     : GOC Automation Platform

import logging
from django.core.cache import caches
from resource_base.modules.importModules import *
from django.core import mail
from operationweb.scripts import disk_utilization_check
from mainweb.models import TimeSavingStatistics
from django.views.decorators.csrf import csrf_exempt
from operationweb.scripts import email_factory

# Get the django logger
logger = logging.getLogger('django')


def disk_utilization_check_index(request):
    return render(request, 'operation/disk_utilization_check.html')


def disk_utilization_check_execute(request):
    try:
        # Get the request data
        rec = request.POST
        loginid = request.session['user_account']['loginid']
        nt_password = rec.get('ntPassword')
        host_list = rec.get('hostList').strip().split(',')

        logger.info(request.session.get('user_account')['loginid'] + ' is checking disk utilization for: %s' % (
        str(host_list),))

        free_space_list_result = disk_utilization_check.disk_utilization_check(host_list, loginid, nt_password, '1')

        logger.info('Disk check result: ' + str(free_space_list_result))

    except Exception as e:
        logger.error('Error checking disk utilization: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    # Time saving statistic
    TimeSavingStatistics.time_saving_statistic('disk_utilization_check', 390)
    return JsonResponse({'status': True, 'data': free_space_list_result})


@csrf_exempt
def disk_utilization_disk_clean_execute(request):
    try:
        # Get the request data
        rec = request.POST
        loginid = request.session['user_account']['loginid']
        nt_password = rec.get('ntPassword')
        host_name = rec.get('hostName').lower()

        logger.info(request.session.get('user_account')['loginid'] + ' is cleaning disk for: %s' % (str(host_name),))

        disk_clean_result = disk_utilization_check.disk_utilization_check([host_name,], loginid, nt_password, '2')

        logger.info('Disk clean result: ' + str(disk_clean_result))

    except Exception as e:
        logger.error('Error cleaning disk: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    # Time saving statistic
    TimeSavingStatistics.time_saving_statistic('disk_utilization_check', 180)
    return JsonResponse({'status': True, 'data': disk_clean_result})


@csrf_exempt
def disk_utilization_disk_size_list_execute(request):
    try:
        # Use CACHES default settings in settings.py
        cache = caches['default']
        # Get the request data
        rec = request.POST
        loginid = request.session['user_account']['loginid']
        nt_password = rec.get('ntPassword')
        host_name = rec.get('hostName').lower()

        logger.info(request.session.get('user_account')['loginid'] + ' is listing disk size for: %s' % (str(host_name),))

        disk_size_list_result = disk_utilization_check.disk_utilization_check([host_name,], loginid, nt_password, '3')

        # Save disk size list to Redis
        cache.set(host_name + '_disk_size_list', disk_size_list_result[0][host_name], 30 * 60)

        logger.info('Disk size list result: ' + str(disk_size_list_result))

    except Exception as e:
        logger.error('Error listing disk size: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    # Time saving statistic
    TimeSavingStatistics.time_saving_statistic('disk_utilization_check', 780)
    return JsonResponse({'status': True, 'data': disk_size_list_result})


def disk_utilization_send_email(request):
    try:
        # Use CACHES default settings in settings.py
        cache = caches['default']
        rec = request.POST
        loginid = request.session['user_account']['loginid']
        host_name = rec.get('host_name').lower()

        disk_size_list = cache.get(host_name + '_disk_size_list')

        from_email = 'CI-Server-Operation-Center@cn.bosch.com'
        cc_email = ['CI-Server-Operation-Center@cn.bosch.com']
        host_used_by = cache.get(host_name + "_used_by")

        # Get the Email subject and content from email_factory
        email_msg = email_factory.get_disk_utilization_notification(host_name, disk_size_list)

        logger.info(host_used_by)


        # Initiate the Email message by EmailMessage
        msg = mail.EmailMessage(subject=email_msg['subject'], body=email_msg['content'],
                            from_email=from_email, to=host_used_by.split('; '),
                            cc=cc_email)
        # Adjust the Email content type to html
        msg.content_subtype = 'html'
        delivered_mails = msg.send()

        logger.info(str(delivered_mails) + 'Emails have been sent successfully.')
    
    except Exception as e:
        logger.error('Error sending Email: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})
    
    # Time saving statistic
    TimeSavingStatistics.time_saving_statistic('disk_utilization_check', 180)
    return JsonResponse({'status': True})
