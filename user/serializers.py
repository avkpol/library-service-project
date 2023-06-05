from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenRefreshSerializer
)
from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'is_staff')


    def create(self, validated_data):
        password = validated_data.pop('password')
        customer = Customer(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'email', 'first_name', 'last_name')


class LoginSerializer(TokenObtainPairSerializer):
    pass


class LogoutSerializer(TokenRefreshSerializer):
    pass