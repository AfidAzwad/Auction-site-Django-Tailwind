from django.urls import path, include
from .views import LoginAPIView, RegisterAPIView, AccountActivateView


urlpatterns = [
     path('user/login', LoginAPIView.as_view(), name='login'),
     path('user/register', RegisterAPIView.as_view(), name='register'),
     path('user/activate/<str:uidb64>/<str:token>/', AccountActivateView.as_view(), name='activate_account'),
]
