from django.urls import path,include
from .api_views import *
from rest_framework import routers
from knox import views as knox_views
from .api_views import LoginView

# router=routers.DefaultRouter()
# router.register('login', LoginApi, basename='login_view')
# router.register('logout', LogoutApi, basename='logout')


urlpatterns = [
    path('dispatch/location/', DispatchesLocationAPI.as_view(), name='DispatchesLocationAPI'),

    #mobile api urls starts...
    # path('api/', include(router.urls) )
    
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('register/', RegisterAPI.as_view(), name = 'register_api'),
    path('profile/', Profile.as_view(), name = 'profile_api'),
    path('profile/update/', UpdateProfile.as_view(), name = 'update_profile_api'),
    path('dispatch/list/', DispatchList.as_view(), name = 'dispatch_list_api'),
    path('change/password/', ChangePasswordView.as_view(), name = 'change_pass_api'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
