from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenRefreshSerializer
)
from rest_framework import serializers
from .models import Customer


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user



class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password', 'is_staff')

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = validated_data.pop('username')

        try:
            customer = Customer.objects.get(username=username)
            raise serializers.ValidationError('A customer with this username already exists.')
        except Customer.DoesNotExist:
            customer = Customer.objects.create_user(username=username, email=email, **validated_data, is_active=True)
            customer.set_password(password)
            customer.save()

        return customer


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class LoginSerializer(TokenObtainPairSerializer):
    pass


class LogoutSerializer(TokenRefreshSerializer):
    pass