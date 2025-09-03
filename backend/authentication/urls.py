from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

<<<<<<< Updated upstream
from .views import SignInView, SignUpView, SignOutView, PasswordChangeView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('signin/', SignInView.as_view(), name='signin'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signout/', SignOutView.as_view(), name='signout'),
    path('password-change/', PasswordChangeView.as_view(), name='passwordchange'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='passwordresetrequest'),
    path('password-reset-confirmation/', PasswordResetConfirmView.as_view(), name='passwordresetconfirmation'),
    path('token/refresh/', TokenRefreshView.as_view(), name='tokenrefresh'),
=======
from .views import SignUpView, SignInView, SignOutView, UserProfileView, TokenRefreshView, DashboardView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name = 'signup'),
    path('signin/', SignInView.as_view(), name = 'signin'),
    path('signout/', SignOutView.as_view(), name = 'signout'),
    path('profile/', UserProfileView.as_view(), name = 'profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('dashboard/', DashboardView.as_view(), name = 'dashboard'),
>>>>>>> Stashed changes
]
