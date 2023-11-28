from django.urls import path, re_path

from . import views

urlpatterns = [
    path('api-auth-token/', views.AuthTokenLogin.as_view(), name='login'),
    path('api-token-auth/validate/', views.AuthLoginStep.as_view(), name='login_step'),
    path('api-auth-register/', views.AuthRegister.as_view(), name='register'),
    path('api-auth-user/profile/', views.AuthUserProfile.as_view(), name='profile'),
    path('api-auth-user/password_change/', views.AuthPasswordChange.as_view(), name='password_change'),
    path('api-auth-user/password_reset/', views.PasswordResetRequest.as_view(), name='password_reset'),
    path('api-auth-user/activate_request/<int:pk>/', views.ActivationRequest.as_view(), name='verification_request'),
    re_path(r'^api-auth-user/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,35})/$',
            views.AccountActivation.as_view(), name='activate'),
    re_path(r'^api-auth-user/password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,35})/$',
            views.ResetPasswordConfirm.as_view(), name='password_reset_confirm'),
]