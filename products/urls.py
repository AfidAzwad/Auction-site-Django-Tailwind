from django.urls import path
from .category_product_view import ProductViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = router.urls