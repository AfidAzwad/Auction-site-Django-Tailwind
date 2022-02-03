from django.urls import path
from . import views
from .views import RegistrationView, LogoutView, VerificationView, LoginView, RequestPasswordReset, CompletePasswordReset
from django.contrib.auth import views as auth_views

app_name = "accounts"


urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('request-reset-link', RequestPasswordReset.as_view(), name="request-reset-link"),
    path('set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name="set-new-password"),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),
]
