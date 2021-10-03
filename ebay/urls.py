from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "ebay"


urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('admin/', views.adminlogin, name="adminlogin"),
    path('admindash/', views.adminDash, name="admindash"),
    # path('customer/', views.customers, name="customer"),
    path('addproduct/', views.addproducts, name="addproduct"),
    # path('myproduct/', views.myproduct, name="myproduct"),
    path('update/<int:pid>/', views.update, name="update"),
    path('<int:pid>/', views.deletion, name="delete"), 
    # path('productinfo/<int:pid>/', views.productinfo, name="productinfo"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
