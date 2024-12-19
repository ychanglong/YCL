from django.urls import path
from pmcweb.views import pmc_coordination, pmc_operation, pmc_hardware_search, pmc_backup_schedule

# urls for userweb app
urlpatterns = [
    # default: pmc/
    # PMC new request
    path("pmc_coordination/pmc_new_request_index/", pmc_coordination.pmc_new_request_index, name="pmc_new_request_index"),
    path("pmc_coordination/new_request_get_assignee/", pmc_coordination.new_request_get_assignee, name="new_request_get_assignee"),
    path("pmc_coordination/new_request_get_pmc_coordinator/", pmc_coordination.new_request_get_pmc_coordinator, name="new_request_get_pmc_coordinator"),
    path("pmc_coordination/new_request_get_itsp_data/", pmc_coordination.new_request_get_itsp_data, name="new_request_get_itsp_data"),
    path("pmc_coordination/new_request_save_activity_plan/", pmc_coordination.new_request_save_activity_plan, name="new_request_save_activity_plan"),

    # PMC view request
    path("pmc_coordination/pmc_view_request_index/", pmc_coordination.pmc_view_request_index, name="pmc_view_request_index"),
    path("pmc_coordination/view_request_search_activity/", pmc_coordination.view_request_search_activity, name="view_request_search_activity"),
    path("pmc_coordination/view_request_delete_activity/", pmc_coordination.view_request_delete_activity, name="view_request_delete_activity"),
    path("pmc_coordination/view_request_get_activity/", pmc_coordination.view_request_get_activity, name="view_request_get_activity"),

    # PMC edit request
    path("pmc_coordination/pmc_edit_request_index/", pmc_coordination.pmc_edit_request_index, name="pmc_edit_request_index"),
    path("pmc_coordination/edit_request_save_activity/", pmc_coordination.edit_request_save_activity, name="edit_request_save_activity"),
    path("pmc_coordination/edit_request_get_device_list/", pmc_coordination.edit_request_get_device_list, name="edit_request_get_device_list"),
    path("pmc_coordination/edit_request_view_device_list/", pmc_coordination.edit_request_view_device_list, name="edit_request_view_device_list"),
    path("pmc_coordination/edit_request_save_device_list/", pmc_coordination.edit_request_save_device_list, name="edit_request_save_device_list"),
    path("pmc_coordination/edit_request_pmc_confirm/", pmc_coordination.edit_request_pmc_confirm, name="edit_request_pmc_confirm"),

    # PMC Public view
    path("pmc_coordination/pmc_public_view_index/", pmc_coordination.pmc_public_view_index, name="pmc_public_view_index"),
    path("pmc_coordination/pmc_public_view_search_activity/", pmc_coordination.pmc_public_view_search_activity, name="pmc_public_view_search_activity"),

    # PMC operation
    path("pmc_operation/pmc_operation_index/", pmc_operation.pmc_operation_index, name="pmc_operation_index"),
    path("pmc_operation/pmc_operation_search_activity/", pmc_operation.pmc_operation_search_activity, name="pmc_operation_search_activity"),
    path("pmc_operation/pmc_operation_execute/", pmc_operation.pmc_operation_execute, name="pmc_operation_execute"),
    path("pmc_operation/pmc_operation_execution_log/", pmc_operation.pmc_operation_execution_log, name="pmc_operation_execution_log"),

    # PMC hardware search
    path("pmc_hardware_search/pmc_hardware_search_index/", pmc_hardware_search.pmc_hardware_search_index, name="pmc_hardware_search_index"),
    path("pmc_hardware_search/pmc_hardware_search_handle/", pmc_hardware_search.pmc_hardware_search_handle, name="pmc_hardware_search_handle"),

    # PMC backup schedule
    path("pmc_backup_schedule/pmc_backup_schedule_index/", pmc_backup_schedule.pmc_backup_schedule_index, name="pmc_backup_schedule_index"),
    path("pmc_backup_schedule/pmc_backup_schedule_search_schedule/", pmc_backup_schedule.pmc_backup_schedule_search_schedule, name="pmc_backup_schedule_search_schedule"),
    path("pmc_backup_schedule/pmc_backup_schedule_cancel_schedule/", pmc_backup_schedule.pmc_backup_schedule_cancel_schedule, name="pmc_backup_schedule_cancel_schedule"),
    path("pmc_backup_schedule/pmc_backup_schedule_change_schedule/", pmc_backup_schedule.pmc_backup_schedule_change_schedule, name="pmc_backup_schedule_change_schedule"),

]
