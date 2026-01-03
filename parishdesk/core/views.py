from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import ChurchRole, Church
from .serializers import ChurchSerializer, UserSerializer, RegisterSerializer, ChurchRoleSerializer, CustomTokenObtainPairSerializer
from .selectors import list_churches, get_user_church_role
from .services import create_church, assign_role
from .permissions import IsSuperUserOrReadOnly, IsChurchAdmin, HasChurchRole
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
)


class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    @extend_schema(
            tags=["Auth"],
            summary="Login and obtain JWT tokens",
            description="Authenticate a user and return access and refresh JWT tokens.",
        )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

@extend_schema_view(
    list=extend_schema(tags=["Churches"], summary="List churches"),
    retrieve=extend_schema(tags=["Churches"], summary="Retrieve a church"),
    create=extend_schema(tags=["Churches"], summary="Create a church"),
    update=extend_schema(tags=["Churches"], summary="Update a church"),
    partial_update=extend_schema(tags=["Churches"], summary="Partially update a church"),
    destroy=extend_schema(tags=["Churches"], summary="Delete a church"),
)

class ChurchViewSet(viewsets.ModelViewSet):
    queryset = Church.objects.all()
    serializer_class = ChurchSerializer
    permission_classes = [IsSuperUserOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        instance = serializer.save(created_by=user)

        # Assign admin role
        ChurchRole.objects.create(user=user, church=instance, role="Admin", assigned_by=user)

@extend_schema_view(
    list=extend_schema(tags=["Users"], summary="List users"),
    retrieve=extend_schema(tags=["Users"], summary="Retrieve a user"),
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Users"],
        summary="Get current user profile",
    )
    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated], url_path="profile")
    def profile(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class AuthRegisterView(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        tags=["Auth"],
        summary="Register a new user",
        request=RegisterSerializer,
        responses={201: UserSerializer},
    )

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token_serializer = CustomTokenObtainPairSerializer(
            data={
                "username": user.username,
                "password": request.data["password"],
            }
        )

        token_serializer.is_valid(raise_exception=True)
        print(token_serializer)

        # return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(
            token_serializer.validated_data,
            status=status.HTTP_201_CREATED,
        )

@extend_schema_view(
    list=extend_schema(tags=["Roles"], summary="List church roles"),
    retrieve=extend_schema(tags=["Roles"], summary="Retrieve a role"),
    destroy=extend_schema(tags=["Roles"], summary="Remove a role"),
)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = ChurchRole.objects.all()
    serializer_class = ChurchRoleSerializer
    permission_classes = [IsChurchAdmin]

    @extend_schema(
        tags=["Roles"],
        summary="Assign a role to a user in a church",
    )

    def create(self, request, *args, **kwargs):
        # Only church admins can assign roles (enorced in InChurchAdmin)
        user_id = request.data.get("user")
        church_id = request.data.get("church")
        role = request.data.get("role")
        assigned_by = request.user
        user = User.objects.get(pk=user_id)
        church = Church.objects.get(pk=church_id)
        obj = assign_role(user, church, role, assigned_by)
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
