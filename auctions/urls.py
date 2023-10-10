from django.urls import path
from .auction_view import AuctionViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', AuctionViewSet)

urlpatterns = router.urls
