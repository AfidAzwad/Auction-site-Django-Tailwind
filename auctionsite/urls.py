from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('ebay.urls')),
    path('user/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('django.contrib.auth.urls')),

    # it will include the following URL patterns:
    #   accounts/login/ [name='login']
    #   accounts/logout/ [name='logout']
    #   accounts/password_change/ [name='password_change']
    #   accounts/password_change/done/ [name='password_change_done']
    #   accounts/password_reset/ [name='password_reset']
    #   accounts/password_reset/done/ [name='password_reset_done']
    #   accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    #   accounts/reset/done/ [name='password_reset_complete']
]
