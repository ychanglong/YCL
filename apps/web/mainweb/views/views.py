# -*- coding: utf-8 -*-
# @Time        : 2023/03/01
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Main
# @Project     : GOC Automation Platform

from resource_base.modules.importModules import *
from operator import itemgetter
from mainweb.models import APIVisitStatistics, HostsStatistics, TimeSavingStatistics
from userweb.models import Account
from pmcweb.models import PMCActivities
from django.views.decorators.csrf import csrf_exempt
import logging

# Get the django logger
logger = logging.getLogger('django')


def index(request):
    """Return main page
            Args:
                request
            Returns:
                Render to main main.html
    """
    return render(request, 'main/main.html')


def faq_index(request):
    """Return faq page
            Args:
                request
            Returns:
                Render to main faq.html
    """
    return render(request, 'main/faq.html')


def change_log_index(request):
    """Return change_log page
            Args:
                request
            Returns:
                Render to main change_log.html
    """
    return render(request, 'main/change_log.html')


def home_view(request):
    """Return main_home page
            Args:
                request
            Returns:
                Render to main main_home.html
    """
    return render(request, 'main/main_home.html')


@csrf_exempt
def api_requests_chart(request):
    day_select = request.POST.get('daySelect')

    # Get the date in time array format
    seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=int(day_select)))
    # Convert to timestamp
    time_stamp = int(time.mktime(seven_days_ago.timetuple()))

    # Get API visit statistics data
    all_statistics_data = list(APIVisitStatistics.objects.filter(request_time__gte=time_stamp))

    chart_data = {}

    for data in all_statistics_data:
        req_date = time.strftime('%Y-%m-%d', time.localtime(data.request_time))
        amount_dict = {'icinga_amount': 0, 'netiq_amount': 0, 'cmdb_amount': 0}
        if req_date not in chart_data.keys():
            chart_data[req_date] = amount_dict
        else:
            amount_dict = chart_data[req_date]

        if data.service_name == 'ICINGA':
            amount_dict['icinga_amount'] += data.request_amount
        elif data.service_name == 'NETIQ':
            amount_dict['netiq_amount'] += data.request_amount
        elif data.service_name == 'CMDB':
            amount_dict['cmdb_amount'] += data.request_amount
        chart_data[req_date] = amount_dict

    date_list = list(chart_data.keys())
    icinga_amount_list = []
    netiq_amount_list = []
    cmdb_amount_list = []

    for date in date_list:
        icinga_amount_list.append(chart_data[date]['icinga_amount'])
        netiq_amount_list.append(chart_data[date]['netiq_amount'])
        cmdb_amount_list.append(chart_data[date]['cmdb_amount'])

    return JsonResponse({'status': True, 'date_list': date_list, 'icinga_amount_list': icinga_amount_list, 'netiq_amount_list': netiq_amount_list, 'cmdb_amount_list': cmdb_amount_list})


@csrf_exempt
def active_hosts_chart(request):

    try:
        day_select = request.POST.get('daySelect')

        # Get the date in time array format
        seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=int(day_select)))
        # Convert to timestamp
        time_stamp = int(time.mktime(seven_days_ago.timetuple()))

        # Get API visit statistics data
        all_statistics_data = list(HostsStatistics.objects.filter(statistic_time__gte=time_stamp).order_by('-statistic_time'))

        chart_data = {}

        for data in all_statistics_data:
            statistic_date = time.strftime('%Y-%m-%d', time.localtime(data.statistic_time))
            amount_dict = {'unix_amount': 0, 'windows_amount': 0}
            if statistic_date not in chart_data.keys():
                chart_data[statistic_date] = amount_dict
            else:
                amount_dict = chart_data[statistic_date]

            if data.os_type == 'unix_server':
                amount_dict['unix_amount'] = data.quantity
            elif data.os_type == 'windows_server':
                amount_dict['windows_amount'] = data.quantity
            chart_data[statistic_date] = amount_dict

        date_list = list(chart_data.keys())
        unix_amount_list = []
        windows_amount_list = []
        percentage_increase = 0

        for date in date_list:
            unix_amount_list.append(chart_data[date]['unix_amount'])
            windows_amount_list.append(chart_data[date]['windows_amount'])

        if unix_amount_list and windows_amount_list:
            today_total_amount = unix_amount_list[0] + windows_amount_list[0]
            if len(unix_amount_list) > 1 and len(windows_amount_list) > 1:
                yesterday_total_amount = unix_amount_list[1] + windows_amount_list[1]
                percentage_increase = round(((today_total_amount - yesterday_total_amount) / yesterday_total_amount) * 100, 2)
    except Exception as e:
        logger.error('Error getting host statistic data: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True, 'date_list': date_list, 'unix_amount_list': unix_amount_list,
                         'windows_amount_list': windows_amount_list, 'percentage_increase': percentage_increase})


@csrf_exempt
def pmc_tasks_chart(request):

    try:
        # Get the date in time array format
        seven_days_future = (datetime.datetime.now() + datetime.timedelta(days=int(7)))
        # Convert to timestamp
        time_stamp_now = int(time.mktime(datetime.datetime.now().timetuple()))
        time_stamp_seven_days_future = int(time.mktime(seven_days_future.timetuple()))
        seven_days_pmc_data = list(PMCActivities.objects.filter(Q(start_time__gte=time_stamp_now) & Q(start_time__lte=time_stamp_seven_days_future) & Q(data_status=1)))

        pmc_chart_data_list = []

        for data in seven_days_pmc_data:
            pmc_dict = {'pmc_id': data.pmc_id, 'change_number': data.change_number, 'start_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data.start_time)), 'region': data.region, 'data_center_room': data.data_center_room}
            pmc_chart_data_list.append(pmc_dict)

        pmc_chart_data_list.sort(key=itemgetter('start_time'), reverse=False)

        logger.info('Seven days PMC tasks: ' + str(pmc_chart_data_list))
    except Exception as e:
        logger.error('Error retrieving PMC Tasks Chart data: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True, 'data': pmc_chart_data_list})


@csrf_exempt
def online_engineers_chart(request):

    try:
        hour_select = request.POST.get('hourSelect')
        # Get the date in time array format
        select_hours_ago = (datetime.datetime.now() - datetime.timedelta(hours=int(hour_select)))
        # Convert to timestamp
        time_stamp_now = int(time.mktime(datetime.datetime.now().timetuple()))
        time_stamp_select_hours_ago = int(time.mktime(select_hours_ago.timetuple()))

        select_hours_login_users_count = Account.objects.filter(Q(last_login__lte=time_stamp_now) & Q(last_login__gte=time_stamp_select_hours_ago)).count()

        all_users_count = Account.objects.all().count()

        online_rate = round((select_hours_login_users_count / all_users_count) * 100, 0)

        logger.info('Last ' + hour_select + ' hours online users: ' + str(select_hours_login_users_count))
        logger.info('Online rate: ' + str(online_rate))

    except Exception as e:
        logger.error('Error getting online engineers chart data: ' + str(e))
        return JsonResponse({'status': False, 'error': str(e)})

    return JsonResponse({'status': True, 'total_login_users_count': select_hours_login_users_count, 'online_rate': online_rate})


@csrf_exempt
def time_saving_chart(request):
    day_select = request.POST.get('daySelect')

    # Get the date in time array format
    seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=int(day_select)))
    # Convert to timestamp
    time_stamp = int(time.mktime(seven_days_ago.timetuple()))

    # Get API visit statistics data
    all_statistics_data = list(TimeSavingStatistics.objects.filter(request_time__gte=time_stamp))

    chart_data = {}

    for data in all_statistics_data:
        req_date = time.strftime('%Y-%m-%d', time.localtime(data.request_time))
        app_time_saving_dict = {'host_status': 0, 'maintenance_mode': 0, 'cmdb_search': 0, 'email_service': 0, 'pam_credential': 0, 'ilo_health_check': 0, 'disk_utilization_check': 0, 'pmc_coordination': 0, 'hardware_search': 0}
        if req_date not in chart_data.keys():
            chart_data[req_date] = app_time_saving_dict
        else:
            app_time_saving_dict = chart_data[req_date]

        if data.app_name == 'host_status':
            app_time_saving_dict['host_status'] += round((data.time_saved / 60), 2)
        elif data.app_name == 'maintenance_mode':
            app_time_saving_dict['maintenance_mode'] += round((data.time_saved / 60), 2)
        elif data.app_name == 'cmdb_search':
            app_time_saving_dict['cmdb_search'] += round((data.time_saved / 60), 2)
        elif data.app_name == 'email_service':
            app_time_saving_dict['email_service'] += round((data.time_saved / 60), 2)
        elif data.app_name == 'pam_credential':
            app_time_saving_dict['pam_credential'] += round((data.time_saved / 60), 2)
        elif data.app_name == 'ilo_health_check':
            app_time_saving_dict['ilo_health_check'] += round((data.time_saved / 60), 2)
        elif data.app_name == 'disk_utilization_check':
            app_time_saving_dict['disk_utilization_check'] += round((data.time_saved / 60), 2)
        elif data.app_name == 'pmc_coordination':
            app_time_saving_dict['pmc_coordination'] += round((data.time_saved / 60), 2)
        elif data.app_name == 'hardware_search':
            app_time_saving_dict['hardware_search'] += round((data.time_saved / 60), 2)

        for key, value in app_time_saving_dict.items():
            app_time_saving_dict[key] = round(value, 2)

        chart_data[req_date] = app_time_saving_dict

    date_list = list(chart_data.keys())
    host_status_time_saved_list = []
    maintenance_mode_time_saved_list = []
    cmdb_search_time_saved_list = []
    email_service_time_saved_list = []
    pam_credential_time_saved_list = []
    ilo_health_check_time_saved_list = []
    disk_utilization_check_time_saved_list = []
    pmc_coordination_time_saved_list = []
    hardware_search_time_saved_list = []

    for date in date_list:
        host_status_time_saved_list.append(chart_data[date]['host_status'])
        maintenance_mode_time_saved_list.append(chart_data[date]['maintenance_mode'])
        cmdb_search_time_saved_list.append(chart_data[date]['cmdb_search'])
        email_service_time_saved_list.append(chart_data[date]['email_service'])
        pam_credential_time_saved_list.append(chart_data[date]['pam_credential'])
        ilo_health_check_time_saved_list.append(chart_data[date]['ilo_health_check'])
        disk_utilization_check_time_saved_list.append(chart_data[date]['disk_utilization_check'])
        pmc_coordination_time_saved_list.append(chart_data[date]['pmc_coordination'])
        hardware_search_time_saved_list.append(chart_data[date]['hardware_search'])

    return JsonResponse({'status': True, 'date_list': date_list, 'host_status_time_saved_list': host_status_time_saved_list,
                         'maintenance_mode_time_saved_list': maintenance_mode_time_saved_list, 'cmdb_search_time_saved_list': cmdb_search_time_saved_list,
                         'email_service_time_saved_list': email_service_time_saved_list, 'pam_credential_time_saved_list': pam_credential_time_saved_list,
                         'ilo_health_check_time_saved_list': ilo_health_check_time_saved_list, 'disk_utilization_check_time_saved_list': disk_utilization_check_time_saved_list,
                         'pmc_coordination_time_saved_list': pmc_coordination_time_saved_list, 'hardware_search_time_saved_list': hardware_search_time_saved_list
                         })
