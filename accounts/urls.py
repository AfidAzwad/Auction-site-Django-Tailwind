from django.urls import path
from . import views
from .views import RegistrationView, LogoutView, VerificationView, LoginView


app_name = "accounts"


urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
]
