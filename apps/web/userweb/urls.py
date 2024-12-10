from django.urls import path
from userweb.views import user as user_views
from userweb.views import login as login_views

# urls for userweb app
urlpatterns = [
    # default: user/

    # ==== Profile ====
    path('profile/', user_views.profile_index, name="user_profile_index"),
    path("profile/change_profile", user_views.change_profile, name="user_change_profile"),

    # ==== User Login ====
    path('login/', login_views.index, name='login'),
    path('login/handle/', login_views.login_handle, name='login_handle'),

    # ==== User Logout ====
    path("user_logout/", user_views.user_logout, name="user_logout"),

    # ==== Teammates ====
    path("teammates/", user_views.teammates_index, name="teammates_index"),
    path("teammates/teammates_list", user_views.teammates_list, name="teammates_list"),
    path("teammates/teammates_add", user_views.teammates_add, name="teammates_add"),


]
