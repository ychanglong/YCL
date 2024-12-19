import time
from django.contrib import admin
from mainweb.models import APIVisitStatistics, AppVisitStatistics, HostsStatistics, TimeSavingStatistics

class APIVisitStatisticsAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'api_url', 'request_amount', 'view_request_time')

    # 设置过滤选项
    list_filter = ('api_url',)

    # 每页显示条目数
    list_per_page = 30

    # 设置搜索功能
    search_fields = ['service_name', 'api_url', 'request_amount']

    @admin.display(empty_value='-')
    def view_request_time(self, obj):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(obj.request_time)) if obj.request_time else None


admin.site.register(APIVisitStatistics, APIVisitStatisticsAdmin)


class AppVisitStatisticsAdmin(admin.ModelAdmin):
    list_display = ('app_name', 'app_url', 'request_amount', 'view_statistic_time')

    # 设置过滤选项
    list_filter = ('app_name', 'app_url')

    # 每页显示条目数
    list_per_page = 30

    # 设置搜索功能
    search_fields = ['app_name', 'app_url']

    @admin.display(empty_value='-')
    def view_statistic_time(self, obj):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(obj.statistic_time)) if obj.statistic_time else None


admin.site.register(AppVisitStatistics, AppVisitStatisticsAdmin)


class HostsStatisticsAdmin(admin.ModelAdmin):
    list_display = ('os_type', 'quantity', 'view_statistic_time')

    # 设置过滤选项
    list_filter = ('os_type',)

    # 每页显示条目数
    list_per_page = 30

    # 设置搜索功能
    search_fields = ['os_type', 'view_statistic_time']

    @admin.display(empty_value='-')
    def view_statistic_time(self, obj):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(obj.statistic_time)) if obj.statistic_time else None


admin.site.register(HostsStatistics, HostsStatisticsAdmin)


class TimeSavingStatisticsAdmin(admin.ModelAdmin):
    list_display = ('app_name', 'time_saved', 'request_time')

    # 设置过滤选项
    list_filter = ('app_name', 'request_time',)

    # 每页显示条目数
    list_per_page = 30

    # 设置搜索功能
    search_fields = ['app_name', 'request_time']

    @admin.display(empty_value='-')
    def view_request_time(self, obj):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(obj.request_time)) if obj.request_time else None


admin.site.register(TimeSavingStatistics, TimeSavingStatisticsAdmin)
