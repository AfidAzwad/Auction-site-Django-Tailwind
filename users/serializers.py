from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        

class ActivationSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
