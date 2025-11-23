from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChurchViewSet, UserViewSet, AuthRegisterView, RoleViewSet, ObtainTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r"churches", ChurchViewSet, basename="church")
router.register(r"users", UserViewSet, basename="user")
router.register(r"roles", RoleViewSet, basename="role")
router.register(r"auth", AuthRegisterView, basename="auth-register")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", ObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
