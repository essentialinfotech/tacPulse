from django.urls import path, register_converter
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth import views
from .decorators import forbidden
from Accounts.utils import HashIdConverter
register_converter(HashIdConverter, "hashid")

urlpatterns = [
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),

    path('', dashboard, name='dashboard'),

    path('profile/<hashid:id>/', admin_profile, name='my_profile'),
    path('dispatch/profile/', dispatch_profile, name='dispatch_profile'),
    path('user/profile/', user_profile, name='user_profile'),

    path('chart_admin_profile/', chart_admin_profile, name='chart_admin_profile'),
    path('chart_dispatch_profile,/', chart_dispatch_profile,
         name='chart_dispatch_profile'),

    path('edit/profile/', edit_profile_admin, name='edit_profile_admin'),
    path('edit/profile/dispatch/', edit_profile_dispatch,
         name='edit_profile_dispatch'),
    path('edit/profile/user/', edit_profile_user, name='edit_profile_user'),

    path('registration/', register, name='register'),

    path('reset/password/', reset_password, name='reset_password'),
    path('forbidden/', forbidden, name='forbidden'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
