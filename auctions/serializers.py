from rest_framework import serializers
from .models import AUCTION, BID



class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AUCTION
        fields = fields = '__all__'
    
    
class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = BID
        fields = '__all__'
