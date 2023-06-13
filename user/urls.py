from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user.views import CustomerViewSet, AuthViewSet
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r"auth", AuthViewSet, basename="auth")
router.register("users", CustomerViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),

    # path("users/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('token/refresh/', CustomerViewSet.as_view({'post': 'logout'}), name='token-refresh'),
    # path('users/token/refresh/', LogOutView.as_view(), name='token-refresh'),

]


app_name = "user"

"""
    # path('users/token/refresh/', CustomerViewSet.as_view({'post': 'refresh'}), name='token-refresh'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/', AuthViewSet.as_view({'post': 'create'}), name='user-login'),
    # path('auth/logout/', AuthViewSet.as_view({'post': 'destroy'}), name='user-logout'),
    # path('users/register/', CustomerRegistrationView.as_view(), name='user-registration'),
"""
