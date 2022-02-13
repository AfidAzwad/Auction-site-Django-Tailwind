from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "ebay"


urlpatterns = [
    path('', views.home, name="home"),
    path('allproduct/', views.allproduct, name="allproduct"),
    path('addproduct/', views.addproducts, name="addproduct"),
    path('myproduct/', views.myproduct, name="myproduct"),
    path('update/<int:pid>/', views.update, name="update"),
    path('<int:pid>/', views.deletion, name="delete"),
    path('productinfo/<int:pid>/', views.productinfo, name="productinfo"),
    path('mybids/', views.mybids, name="mybids"),
    path('bid/<int:serial>/', views.biddelete, name="biddelete"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
