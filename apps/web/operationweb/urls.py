from django.urls import path
from operationweb.views import email_service, pam_credential, cmdb_search, ilo_health_check, disk_utilization_check, os_service_check, win_hotfix_check

# urls for operationweb app
urlpatterns = [
    path("email_service/", email_service.email_service_index, name="email_service_index"),
    path("email_service/email_service_send", email_service.email_service_send, name="email_service_send"),
    path("pam_credential/", pam_credential.pam_credential_index, name="pam_credential_index"),
    path("pam_credential/pam_credential_search", pam_credential.pam_credential_search, name="pam_credential_search"),
    path("cmdb_search/", cmdb_search.cmdb_search_index, name="cmdb_search_index"),
    path("cmdb_search/cmdb_search_handle", cmdb_search.cmdb_search_handle, name="cmdb_search_handle"),
    path("ilo_health_check/", ilo_health_check.ilo_health_check_index, name="ilo_health_check_index"),
    path("ilo_health_check/ilo_health_check_execute", ilo_health_check.ilo_health_check_execute, name="ilo_health_check_execute"),
    path("ilo_health_check/ilo_health_detail", ilo_health_check.ilo_health_detail, name="ilo_health_detail"),
    path("ilo_health_check/ilo_reset_ilo", ilo_health_check.ilo_reset_ilo, name="ilo_reset_ilo"),
    path("ilo_health_check/ilo_get_iml", ilo_health_check.ilo_get_iml, name="ilo_get_iml"),
    path("ilo_health_check/ilo_get_ahs", ilo_health_check.ilo_get_ahs, name="ilo_get_ahs"),
    path("disk_utilization_check_index/", disk_utilization_check.disk_utilization_check_index, name="disk_utilization_check_index"),
    path("disk_utilization_check_index/disk_utilization_check_execute", disk_utilization_check.disk_utilization_check_execute, name="disk_utilization_check_execute"),
    path("disk_utilization_check_index/disk_utilization_disk_clean_execute", disk_utilization_check.disk_utilization_disk_clean_execute, name="disk_utilization_disk_clean_execute"),
    path("disk_utilization_check_index/disk_utilization_disk_size_list_execute", disk_utilization_check.disk_utilization_disk_size_list_execute, name="disk_utilization_disk_size_list_execute"),
    path("disk_utilization_check_index/disk_utilization_send_email", disk_utilization_check.disk_utilization_send_email, name="disk_utilization_send_email"),
    path("os_service_check_index/", os_service_check.os_service_check_index, name="os_service_check_index"),
    path("os_service_check_index/os_service_check_execute", os_service_check.os_service_check_execute, name="os_service_check_execute"),
    path("win_hotfix_check_index/", win_hotfix_check.win_hotfix_check_index, name="win_hotfix_check_index"),
    path("win_hotfix_check_index/win_hotfix_check_execute", win_hotfix_check.win_hotfix_check_execute, name="win_hotfix_check_execute"),
    path("win_hotfix_check_index/win_hotfix_list_execute", win_hotfix_check.win_hotfix_list_execute, name="win_hotfix_list_execute"),

]
