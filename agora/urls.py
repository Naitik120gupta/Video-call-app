from django.urls import path
from . import views
from .views import RegisterView, LoginView, PasswordResetRequestView,SetNewPasswordView



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set_new_password'),

    path('', views.lobby),
    path('room/', views.room),
    path('get_token/', views.getToken),

    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),
]