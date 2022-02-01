from django.urls import path
from . import views
from .views import RegistrationView, LogoutView, VerificationView, LoginView, RequestPasswordReset, CompletePasswordReset


app_name = "accounts"


urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('request-reset-link', RequestPasswordReset.as_view(), name="request-reset-link"),
    path('set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name="set-new-password"),
]
