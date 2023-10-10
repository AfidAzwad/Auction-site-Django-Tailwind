from django.urls import path
from .auction_view import AuctionViewSet
from .bid_view import BIDViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'auction', AuctionViewSet)
router.register(r'bid', BIDViewSet)

urlpatterns = router.urls
