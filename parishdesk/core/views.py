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

class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ChurchViewSet(viewsets.ModelViewSet):
    queryset = Church.objects.all()
    serializer_class = ChurchSerializer
    permission_classes = [IsSuperUserOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        instance = serializer.save(created_by=user)

        # Assign admin role
        ChurchRole.objects.create(user=user, church=instance, role="Admin", assigned_by=user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated], url_path="/me")
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class AuthRegisterView(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"], url_path="/register")
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = ChurchRole.objects.all()
    serializer_class = ChurchRoleSerializer
    permission_classes = [IsChurchAdmin]

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
