from django.urls import path
from mainweb.views import views as main_views

# urls for mainweb app
urlpatterns = [
    # default: main/
    path("", main_views.index, name="main"),
    path("home_view/", main_views.home_view, name="main_home"),
    path("faq_index/", main_views.faq_index, name="faq_index"),
    path("change_log_index/", main_views.change_log_index, name="change_log_index"),
    path("api_requests_chart/", main_views.api_requests_chart, name="api_requests_chart"),
    path("active_hosts_chart/", main_views.active_hosts_chart, name="active_hosts_chart"),
    path("pmc_tasks_chart/", main_views.pmc_tasks_chart, name="pmc_tasks_chart"),
    path("online_engineers_chart/", main_views.online_engineers_chart, name="online_engineers_chart"),
    path("time_saving_chart/", main_views.time_saving_chart, name="time_saving_chart"),
]
