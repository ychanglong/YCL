# -*- coding: utf-8 -*-
# @Time        : 2024/10/10
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : PMC
# @Project     : GOC Automation Platform

from resource_base.modules.importModules import *
from mainweb.models import TimeSavingStatistics
from pmcweb.models import PMCBackupschedule
from operator import itemgetter
from pmcweb.scripts import backup_request
import arrow
import logging

# Get the django logger
logger = logging.getLogger('django')


def pmc_backup_schedule_index(request):
    """Return pmc backup schedule page
        Args:
            request
        Returns:
            Render to pmc_backup_schedule.html
    """
    return render(request, 'pmc/pmc_backup_schedule.html')


def pmc_backup_schedule_search_schedule(request):
    try:
        rec = request.POST
        pmc_backup_schedule_status = rec.getlist('searchBackupScheduleStatus')
        pmc_status = rec.getlist('searchPMCStatus')
        pmc_change_number = rec.get('searchChangeNumber')
        user_timezone = request.session.get('user_account')['timezone']

        logger.info(request.session.get('user_account')['loginid'] + ' is searching PMC data for: %s %s %s' % (str(pmc_status), str(pmc_backup_schedule_status), str(pmc_change_number)))

        # Get the PMC backup schedule list from DB
        pmc_backup_schedule_list = list(PMCBackupschedule.objects.filter(Q(pmc_activity__status__in=pmc_status if pmc_status else [0,1,2,3,4,5]), Q(schedule_status__in=pmc_backup_schedule_status if pmc_backup_schedule_status else [0,1]), Q(change_number__icontains=pmc_change_number)))

        # Resort the attributes
        sorted_pmc_activities = []
        for schedule in pmc_backup_schedule_list:
            # status: 0: New, 1: In progress, 2: Pending, 3: Scheduled, 4: Completed, 5: Cancelled
            if schedule.pmc_activity.status == 0:
                pmc_status = 'New'
            elif schedule.pmc_activity.status == 1:
                pmc_status = 'In progress'
            elif schedule.pmc_activity.status == 2:
                pmc_status = 'Pending'
            elif schedule.pmc_activity.status == 3:
                pmc_status = 'Scheduled'
            elif schedule.pmc_activity.status == 4:
                pmc_status = 'Completed'
            elif schedule.pmc_activity.status == 5:
                pmc_status = 'Cancelled'
            else:
                pmc_status = 'Unknown'
            
            # status: 0: Cancelled, 1: Scheduled
            if schedule.schedule_status == 0:
                schedule_status = 'Cancelled'
            elif schedule.schedule_status == 1:
                schedule_status = 'Scheduled'
            else:
                schedule_status = 'Unknown'

            activity_temp = {'schedule_id': schedule.schedule_id,
                             'change_number': schedule.change_number,
                             'backup_device_name': schedule.backup_device_name,
                             'start_time': arrow.get(schedule.start_time).to(user_timezone).format('YYYY-MM-DD HH:mm:ss') if schedule.start_time else '-',
                             'end_time': arrow.get(schedule.end_time).to(user_timezone).format('YYYY-MM-DD HH:mm:ss') if schedule.end_time else '-',
                             'schedule_status': schedule_status,
                             'pmc_status': pmc_status,
                             }

            sorted_pmc_activities.append(activity_temp)
            sorted_pmc_activities.sort(key=itemgetter('start_time'), reverse=True)

    except Exception as e:
        logger.error('Error searching PMC backup schedule: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True, 'data': sorted_pmc_activities})


def pmc_backup_schedule_cancel_schedule(request):
    try:
        rec = request.POST
        change_number = rec.get('change_number')
        schedule_id = rec.get('schedule_id')

        # Check user's permission
        if request.session.get('user_account')['guest_account'] == 1:
            return JsonResponse({'status': False, 'error': 'You don\'t have permission to cancel requests.'})

        logger.info(request.session.get('user_account')['loginid'] + ' is canceling PMC backup schedule for: %s %s' % (str(schedule_id), str(change_number)))

        backup_access_token = backup_request.backup_login()

        if backup_access_token:
            if backup_request.backup_schedule_cancel(backup_access_token, schedule_id, change_number):
                # Update the PMC backup schedule status
                pmc_backup_schedule = PMCBackupschedule.objects.get(change_number=change_number, schedule_id=schedule_id)

                if pmc_backup_schedule:
                    pmc_backup_schedule.schedule_status = 0
                    pmc_backup_schedule.save()
                else:
                    return JsonResponse({'status': False, 'error': 'PMC backup schedule not found!'})
            else:
                logger.info('Error canceling PMC backup schedule')
                return JsonResponse({'status': False, 'error': 'Error canceling PMC backup schedule'})
        else:
            logger.info('Error login the backup API to get the access token')
            return JsonResponse({'status': False, 'error': 'Error login the backup API to get the access token'})

    except Exception as e:
        logger.error('Error canceling PMC backup schedule: ' + str(e))
        return JsonResponse({'status': False, 'error': 'Error canceling PMC backup schedule: ' + str(e)})

    return JsonResponse({'status': True})


def pmc_backup_schedule_change_schedule(request):
    try:
        rec = request.POST
        schedule_id = rec.get('schedule_id')
        change_number = rec.get('change_number')
        start_time = rec.get('start_time')
        end_time = rec.get('end_time')
        user_timezone = request.session.get('user_account')['timezone']

        logger.info(request.session.get('user_account')['loginid'] + ' is changing PMC backup schedule for: %s %s' % (str(schedule_id), str(change_number)))

        # Check user's permission
        if request.session.get('user_account')['guest_account'] == 1:
            return JsonResponse({'status': False, 'error': 'You don\'t have permission to cancel requests.'})

        backup_access_token = backup_request.backup_login()

        if backup_access_token:
            # Convert the timezone to CET
            start_time_arrow = arrow.get(start_time, "YYYY-MM-DD HH:mm:ss", tzinfo=user_timezone)
            end_time_arrow = arrow.get(end_time, "YYYY-MM-DD HH:mm:ss", tzinfo=user_timezone)
            start_time_cet = start_time_arrow.to('Europe/Berlin')
            end_time_cet = end_time_arrow.to('Europe/Berlin')

            if backup_request.backup_schedule_change(backup_access_token, schedule_id, change_number, start_time_cet.strftime('%Y-%m-%d %H:%M:%S.%f'), end_time_cet.strftime('%Y-%m-%d %H:%M:%S.%f')):
                # Update the PMC backup schedule time window
                pmc_backup_schedule = PMCBackupschedule.objects.get(change_number=change_number, schedule_id=schedule_id)

                if pmc_backup_schedule:
                    pmc_backup_schedule.start_time = start_time_arrow.timestamp()
                    pmc_backup_schedule.end_time = end_time_arrow.timestamp()
                    pmc_backup_schedule.save()
                else:
                    return JsonResponse({'status': False, 'error': 'PMC backup schedule not found!'})
            else:
                logger.info('Error changing PMC backup schedule')
                return JsonResponse({'status': False, 'error': 'Error changing PMC backup schedule'})
        else:
            logger.info('Error login the backup API to get the access token')
            return JsonResponse({'status': False, 'error': 'Error login the backup API to get the access token'})

    except Exception as e:
        logger.info('Error changing PMC backup schedule: ' + str(e))
        return JsonResponse({'status': False, 'error': 'Error changing PMC backup schedule: ' + str(e)})

    return JsonResponse({'status': True})
