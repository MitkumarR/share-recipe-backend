from django.urls import path
from .views import SignupView, SigninView, ProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('token/refresh/', ProfileView.as_view(), name='token_refresh'),
]