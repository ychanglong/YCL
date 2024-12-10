from django.urls import path
from monitoringweb.views import maintenance_mode, host_status

# urls for monitoringweb app
urlpatterns = [
    # default: monitoring/
    path("maintenance_mode/", maintenance_mode.maintenance_index, name="maintenance_index"),
    path('maintenance_mode/maintenance_execute/', maintenance_mode.maintenance_execute, name="maintenance_execute"),
    path("host_status/", host_status.host_status_index, name="host_status_index"),
    path("host_status/host_search", host_status.host_search, name="host_search"),
    path("host_status/host_status_search", host_status.host_status_search, name="host_status_search"),

]
