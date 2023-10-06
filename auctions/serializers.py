from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    formatted_category_name = serializers.CharField(source='get_formatted_category_name', read_only=True)

    class Meta:
        model = Category
        fields = ['category_id', 'category_name', 'formatted_category_name']
