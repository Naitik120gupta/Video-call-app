from django.urls import path
from . import views
from .views import RegisterView, LoginView, PasswordResetRequestView,SetNewPasswordView,acquire_resource,start_recording,stop_recording,VerifyOTPView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set_new_password'),

    path('', views.lobby),
    path('room/', views.room),
    path('get_token/', views.getToken),

    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),

    path('acquire/', acquire_resource, name='acquire_resource'),
    path('start/', start_recording, name='start_recording'),
    path('stop/', stop_recording, name='stop_recording'),
]