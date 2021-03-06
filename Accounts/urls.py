from django.urls import path, register_converter
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth import views
from .decorators import forbidden, inactive
from Accounts.utils import HashIdConverter
register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),

    path('', landing, name = 'landing'),
    path('dashboard/', dashboard, name='dashboard'),

    path('profile/<hashid:id>/', admin_profile, name='my_profile'),
    path('dispatch/profile/<hashid:id>/',
         dispatch_profile, name='dispatch_profile'),
    path('user/profile/<hashid:id>/', user_profile, name='user_profile'),
    path('medic/profile/<hashid:id>/', medic_profile, name = 'medic_profile'),

    path('monthly_request_chart_ambulance/', monthly_request_chart_ambulance,
         name='monthly_request_chart_ambulance'),

    path('edit/profile/admin/<hashid:id>/',
         edit_profile_admin, name='edit_profile_admin'),
    path('edit/profile/dispatch/<hashid:id>/', edit_profile_dispatch,
         name='edit_profile_dispatch'),
    path('edit/profile/user/<hashid:id>/',
         edit_profile_user, name='edit_profile_user'),
     path('edit/profile/medic/<hashid:id>/', edit_profile_medic, name = 'edit_profile_medic'),

    path('registration/', register, name='register'),

    path('change_pass/', change_pass, name='change_pass'),
    path('forbidden/', forbidden, name='forbidden'),


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


    path('deleting/<hashid:id>/', delete_any_user, name='delete_any_user'),
    path('traversing/profile/to/profile/<hashid:id>/', profile, name='profile'),
    path('deactivae/<hashid:id>/', deactivate, name='deactivate'),
    path('activate/<hashid:id>/', activate, name='activate'),
    path('inactive/', inactive, name='inactive'),
    path('forbidden/', forbidden, name='forbidden'),
    path('track/dispatches/', TrackDispatches.as_view(), name='track_dispatches'),
    path('assesment/form/', assetment_form, name='assetment_form'),
    path('del_assesment/<hashid:id>/', del_assesment, name='del_assesment'),
    path('assessment/<hashid:id>/', assessment_report_individually,
         name='assessment_report_individually'),
    path('assessment/list/', assesment_list_users, name='assesment_list_users'),
    path('edit/assessment/<hashid:id>/',
         assetment_form_edit, name='assetment_form_edit'),
     path('customers/', customer_list, name = 'customer_list'),

     path('message/<hashid:id>/', send_message, name = 'send_message'),
     path('message/deleting/<hashid:id>/', delete_message, name = 'delete_message'),
     path('track/pos/dispatch/', post_pos_dispatch, name = 'post_pos_dispatch' ),
     path('corporate/users/', corporate_users, name = 'corporate_users'),
     path('manage/roles/<int:id>/', manage_role, name = 'manage_role'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
