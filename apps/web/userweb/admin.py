import time
from django.contrib import admin
from userweb.models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('loginid', 'name', 'status', 'admin', 'pmc_coordinator', 'pmc_operator', 'department', 'email', 'view_last_login', 'view_edit_time', 'view_create_time')

    # 设置过滤选项
    list_filter = ('department', 'status', 'admin', 'pmc_coordinator', 'pmc_operator',)

    # 每页显示条目数
    list_per_page = 15

    # 设置可编辑字段
    list_editable = ('status', 'admin', 'pmc_coordinator', 'pmc_operator',)

    # 设置搜索功能
    search_fields = ['loginid', 'name', 'department', 'email', 'last_login', 'create_time', 'edit_time']

    @admin.display(empty_value='-')
    def view_last_login(self, obj):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(obj.last_login)) if obj.last_login else None

    @admin.display(empty_value='-')
    def view_edit_time(self, obj):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(obj.edit_time)) if obj.edit_time else None

    @admin.display(empty_value='-')
    def view_create_time(self, obj):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(obj.create_time)) if obj.create_time else None


# Register your models here.
admin.site.register(Account, AccountAdmin)
