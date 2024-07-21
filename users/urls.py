from django.urls import path
from .views import SignUpView, LoginView, LogOutView, CustomPasswordResetView, CustomPasswordResetConfirmView, \
    CustomPasswordChangeView
from django.contrib.auth.views import PasswordChangeView, \
    PasswordResetDoneView

app_name = "users"
urlpatterns = [
    path("register/", SignUpView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogOutView.as_view(), name="logout"),
    path("password-change/", CustomPasswordChangeView.as_view(), name="password_change"),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]