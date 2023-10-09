from rest_framework import serializers
from .models import CATEGORY, PRODUCT



class CategorySerializer(serializers.ModelSerializer):
    formatted_category_name = serializers.CharField(read_only=True)

    class Meta:
        model = CATEGORY
        fields = ['category_id', 'category_name', 'formatted_category_name']
    
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PRODUCT
        fields = '__all__'
    