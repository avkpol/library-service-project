from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from user.models import Customer
from user.serializers import LoginSerializer, LogoutSerializer
from user.serializers import CustomerSerializer, TokenSerializer, ProfileSerializer



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.action == 'list':
            return []
        else:
            return super().get_permissions()

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


    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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