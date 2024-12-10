import time
from django.contrib import admin
from pmcweb.models import PMCAssignee, PMCActivities, PMCOperation, PMCDevicelist

class PMCAssigneeAdmin(admin.ModelAdmin):
    list_display = ('assignee_id', 'assignee_nt', 'assignee_name', 'assignee_department', 'assignee_email',)

    # 设置过滤选项
    list_filter = ('assignee_department',)

    # 每页显示条目数
    list_per_page = 20

    # 设置搜索功能
    search_fields = ['assignee_nt', 'assignee_name', 'assignee_department', 'assignee_email']


# Register your models here.
admin.site.register(PMCAssignee, PMCAssigneeAdmin)


class PMCActivitiesAdmin(admin.ModelAdmin):
    list_display = ('change_number', 'itsp_no', 'region', 'location_code', 'data_center_room', 'view_start_time', 'view_end_time', 'status', 'san_vnx', 'san_unity', 'san_vplex', 'nas', 'backup', 'oracle_db', 'change_class', 'data_status')

    # 设置过滤选项
    list_filter = ('data_status', 'region', 'location_code', 'data_center_room', 'status', 'san_vnx', 'san_unity', 'san_vplex', 'nas', 'oracle_db', 'change_class')

    # 每页显示条目数
    list_per_page = 20

    # 设置搜索功能
    search_fields = ['change_number', 'region', 'location_code', 'data_center_room', 'view_start_time', 'view_end_time', 'status']

    @admin.display(empty_value='-')
    def view_start_time(self, obj):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(obj.start_time)) if obj.start_time else None

    @admin.display(empty_value='-')
    def view_end_time(self, obj):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(obj.end_time)) if obj.end_time else None


# Register your models here.
admin.site.register(PMCActivities, PMCActivitiesAdmin)


class PMCOperationAdmin(admin.ModelAdmin):
    list_display = ('pmc_id', 'pmc_confirmed', 'device_name', 'ilo_ip', 'vcenter_fqdn', 'esx_flag', 'nas_cluster_flag')

    # 设置过滤选项
    list_filter = ('pmc_id', 'pmc_confirmed', 'vcenter_fqdn', 'esx_flag', 'nas_cluster_flag')

    # 每页显示条目数
    list_per_page = 30

    # 设置搜索功能
    search_fields = ['pmc_id', 'device_name', 'vcenter_fqdn']


# Register your models here.
admin.site.register(PMCOperation, PMCOperationAdmin)


class PMCDevicelistAdmin(admin.ModelAdmin):
    list_display = ('pmc_id', 'device_name', 'ilo_ip', 'vcenter', 'data_center_room', 'ci_type', 'tier_2', 'tier_3', 'status', 'support_group')

    # 设置过滤选项
    list_filter = ('pmc_id', 'vcenter', 'data_center_room', 'ci_type')

    # 每页显示条目数
    list_per_page = 30

    # 设置搜索功能
    search_fields = ['pmc_id', 'device_name', 'data_center_room', 'ilo_ip']


# Register your models here.
admin.site.register(PMCDevicelist, PMCDevicelistAdmin)