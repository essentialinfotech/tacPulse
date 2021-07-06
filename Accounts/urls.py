from django.urls import path, register_converter
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth import views
from .decorators import forbidden,inactive
from Accounts.utils import HashIdConverter
register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),

    path('', dashboard, name='dashboard'),

    path('profile/<hashid:id>/', admin_profile, name = 'my_profile'),
    path('dispatch/profile/<hashid:id>/', dispatch_profile, name = 'dispatch_profile'),
    path('user/profile/<hashid:id>/', user_profile, name = 'user_profile'),

    path('chart_admin_profile/', chart_admin_profile, name='chart_admin_profile'),
    path('chart_dispatch_profile,/', chart_dispatch_profile,
         name='chart_dispatch_profile'),

    path('edit/profile/', edit_profile_admin, name='edit_profile_admin'),
    path('edit/profile/dispatch/', edit_profile_dispatch,
         name='edit_profile_dispatch'),
    path('edit/profile/user/', edit_profile_user, name='edit_profile_user'),

    path('registration/', register, name='register'),

    path('change_pass/', change_pass, name = 'change_pass'),
    path('forbidden/', forbidden, name = 'forbidden'),


    # password
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    # not responsive template
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),


    path('deleting/<hashid:id>/', delete_any_user, name = 'delete_any_user'),
    path('traversing/profile/to/profile/<hashid:id>/', profile, name = 'profile'),
    path('deactivae/<hashid:id>/', deactivate, name = 'deactivate'),
    path('activate/<hashid:id>/', activate, name = 'activate'),
    path('inactive/', inactive, name = 'inactive'),
    path('forbidden/', forbidden, name='forbidden'),
    path('track/dispatches/', TrackDispatches.as_view(), name='track_dispatches')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
