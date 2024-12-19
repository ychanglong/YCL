from django.contrib import admin
from monitoringweb.models import HostInfo

class HostInfoAdmin(admin.ModelAdmin):
    list_display = ('host_name', 'status', 'status_reason', 'os_type', 'used_by')

    # 设置过滤选项
    list_filter = ('status', 'status_reason', 'os_type')

    # 每页显示条目数
    list_per_page = 100

    # 设置搜索功能
    search_fields = ['host_name', 'status', 'status_reason', 'os_type', 'used_by']


# Register your models here.
admin.site.register(HostInfo, HostInfoAdmin)
