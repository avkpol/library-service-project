from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user.views import CustomerViewSet, AuthViewSet


router = DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")
router.register("users", CustomerViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path('token/refresh/', CustomerViewSet.as_view({'post': 'logout'}), name='token-refresh'),

]


app_name = "user"
