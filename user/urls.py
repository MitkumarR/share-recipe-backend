from django.urls import path
from .views import SignupView, SigninView, UserProfileView, DeactivateAccountView, ChangePasswordView, \
    DeleteAccountView, ReactivateAccountView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('token/refresh/', UserProfileView.as_view(), name='token_refresh'),

    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('deactivate/', DeactivateAccountView.as_view(), name='deactivate-account'),
    path('reactivate/', ReactivateAccountView.as_view(), name='reactivate-account'),
    path('delete/', DeleteAccountView.as_view(), name='delete-account'),

    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]