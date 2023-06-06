from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action

from user.models import Customer
from user.serializers import (
LoginSerializer, LogoutSerializer,
    CustomerRegistrationSerializer,
)
from user.serializers import CustomerSerializer, TokenSerializer, ProfileSerializer



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.action == 'api/users/register':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def token(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], url_path='token/refresh')
    def refresh_token(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data['refresh']
        try:
            token = RefreshToken(refresh)
            return Response({'access': str(token.access_token)})
        except Exception:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'put', 'patch', 'delete'])
    def me(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied("Authentication credentials were not provided.")

        if request.method == 'GET':
            serializer = ProfileSerializer(request.user)
            return Response(serializer.data)

        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            if request.user != self.request.user:
                raise PermissionDenied("You don't have permission to perform this action.")

            if not request.user.is_active:
                raise PermissionDenied("Your account is not active. Please contact support.")

            if request.method == 'DELETE':
                request.user.delete()
                return Response({'detail': 'Account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

            serializer = ProfileSerializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


User = get_user_model()

class AuthViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = TokenObtainPairView.as_view()(request._request)
        return Response(response.data)

    def destroy(self, request):
        logout(request)
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = TokenRefreshView.as_view()(request._request)
        return Response(response.data)