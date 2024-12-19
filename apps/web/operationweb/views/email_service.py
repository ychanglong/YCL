# -*- coding: utf-8 -*-
# @Time        : 2023/03/01
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Operation Tools
# @Project     : GOC Automation Platform

from resource_base.modules.importModules import *
from django.core.cache import caches
from django.core import mail
from operationweb.scripts import email_factory
from monitoringweb.scripts import netiq_request, icinga_request
from mainweb.models import TimeSavingStatistics
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


def email_service_index(request):
    return render(request, 'operation/email_service.html')


def email_service_send(request):
    """Send Email according to Email type"""

    # Get the request data
    rec = request.POST

    # Set default from and cc Email address
    from_email = 'CI-Server-Operation-Center@cn.bosch.com'
    if rec.get('fromEmail'):
        from_email = rec.get('fromEmail')
    to_email = rec.get('toEmail')
    cc_email = ['CI-Server-Operation-Center@cn.bosch.com']

    # Get Email templates: 1: Disk full, 2: Server reboot: Windows uptime 80 days
    email_type = rec.get('emailType')

    # Get Email tittle and content
    email_content = rec.get('emailContent')
    email_subject = rec.get('emailSubject')

    # Get SMT incident number
    incident = rec.get('incident')

    # logging the action
    logger.info(request.session.get('user_account')['loginid'] + ' is sending Email, type: ' + email_type)

    # Check if there is an incident related
    if incident:
        cc_email.append('smt.reply@de.bosch.com')

    # No host list input and customize Email address also not checked
    if not to_email and not rec.get('hostList'):
        return JsonResponse({'status': False, 'error': 'Please check customize Email address or input host list!'})

    # The number of successfully delivered messages
    delivered_mails = 0

    # Read from Redis
    host_info = {}

    # If there is a host list
    if rec.get('hostList'):

        # Host list
        host_list = rec.get('hostList').split(',')

        # Restrict the number of hosts within 200
        if len(host_list) > 200:
            return JsonResponse({'status': False, 'error': 'Please limit the number of hosts within 200!'})

        cache = caches['default']
        for host in host_list:
            host_used_by = cache.get(host.lower() + "_used_by")
            host_info[host] = host_used_by
        if not host_info:
            return JsonResponse({'status': False, 'error': 'No host info found for provided hosts!'})

    try:
        # Define email msg dict
        email_msg = {}
        # If the Email is sent to host owner
        if not to_email:
            mail_list = []
            mail_connection = mail.get_connection()
            # Send Email by templates
            for host_name, used_by in host_info.items():
                # 0: Customize Email
                if email_type == '0':
                    if incident:
                        email_msg['subject'] = '[' + incident + '] ' + email_subject
                    else:
                        email_msg['subject'] = email_subject
                    email_msg['content'] = email_content

                # Other Email type
                else:
                    # Get the Email subject and content from email_factory
                    email_msg = email_factory.get_email_msg(host_name, used_by, email_type, incident)

                # Initiate the Email message by EmailMessage
                msg = mail.EmailMessage(subject=email_msg['subject'], body=email_msg['content'],
                                   from_email=from_email, to=used_by.split('; '),
                                   cc=cc_email)
                # Adjust the Email content type to html
                msg.content_subtype = 'html'
                mail_list.append(msg)

            delivered_mails = mail_connection.send_messages(mail_list)

        # If the Email is sent to customized address
        else:
            # If input host number is one
            if len(host_info) == 1:

                # Get the input host info
                (host_name, used_by), = host_info.items()

                # 0: Customize Email
                if email_type == '0':
                    if incident:
                        email_msg['subject'] = '[' + incident + '] ' + email_subject
                    else:
                        email_msg['subject'] = email_subject
                    email_msg['content'] = email_content

                # Other Email type
                else:
                    # Get the Email subject and content from email_factory
                    email_msg = email_factory.get_email_msg(host_name, used_by, email_type, incident)
                # Initiate the Email message by EmailMessage
                msg = mail.EmailMessage(subject=email_msg['subject'], body=email_msg['content'],
                                   from_email=from_email, to=to_email.split(';'),
                                   cc=cc_email)
                # Adjust the Email content type to html
                msg.content_subtype = 'html'
                delivered_mails = msg.send()
            elif len(host_info) == 0:
                # 0: Customize Email
                if email_type == '0':
                    if incident:
                        email_msg['subject'] = '[' + incident + '] ' + email_subject
                    else:
                        email_msg['subject'] = email_subject
                    email_msg['content'] = email_content

                # Other Email type
                else:
                    # Get the Email subject and content from email_factory
                    email_msg = email_factory.get_email_msg('', '', email_type, incident)
                # Initiate the Email message by EmailMessage
                msg = mail.EmailMessage(subject=email_msg['subject'], body=email_msg['content'],
                                   from_email=from_email, to=to_email.split(';'),
                                   cc=cc_email)
                # Adjust the Email content type to html
                msg.content_subtype = 'html'
                delivered_mails = msg.send()

            # If the input host number larger than one
            else:
                return JsonResponse({'status': False, 'error': 'Customized Email address option only accept one host input!'})

    except Exception as e:
        logger.error('Error sending an Email: ' + str(e))
        return JsonResponse({'status': False, 'error': 'Error sending an Email: ' + str(e)})

    # Time saving statistic
    TimeSavingStatistics.time_saving_statistic('email_service', delivered_mails * 460)
    return JsonResponse({'status': True, 'data': 'You have ' + str(delivered_mails) + ' message(s) been sent successfully.'})
