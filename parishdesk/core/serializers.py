from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

from .models import Church, ChurchRole, UserProfile

class ChurchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Church
        fields = [
            "id", "name", "address", "district", "phone", "email", "timezone",
            "created_by", "created_at", "updated_at",
        ]

        read_only_fields = [
            "id", "created_by", "created_at", "updated_at"
        ]

class UserSerializer(serializers.ModelSerializer):
    profile_full_name = serializers.CharField(source="profile.full_name", read_only=True)
    profile_phone = serializers.CharField(source="profile.phone", read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "profile_full_name", "profile_phone"
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    full_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "full_name"]

    def create(self, validated_data):
        full_name = validated_data.pop("full_name", "")
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Update Profile
        profile = getattr(user, "profile", None)
        if profile:
            profile.full_name = full_name or user.get_full_name
            profile.save()
        return user

class ChurchRoleSerializer(serializers.ModelSerializer):
    role_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ChurchRole
        fields = ["id", "user", "church", "role", "role_display", "is_active", "assigned_by", "assigned_at"]
        read_only_fields = ["id", "assigned_by", "assigned_at"]

    def get_role_display(self, obj):
        return obj.get_role_display()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extend token payload to include role and current church info
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        roles = list(user.church_roles.filter(is_active=True).values("church_id", "role"))
        token["roles"] = roles
        # I could include default current church if user has one
        return token

    def validate(self, attr):
        data = super().validate(attr)
        # Add additional response data
        data["user"] = UserSerializer(self.user).data
        data["roles"] = list(self.user.roles.filter(is_active=True).values("church_id", "role"))

        return data
