from rest_framework import permissions
from core.models import ChurchRole


class IsPreacherOrAdmin(permissions.BasePermission):
    """
    Allows access only to:
    - Preacher who owns the teaching
    - Church Admin
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False

        # Check if user is the preacher
        if obj.preacher == user:
            return True

        # Check if user is an admin in the same church
        return ChurchRole.objects.filter(
            user=user,
            church=obj.church,
            role="ADMIN",
            is_active=True,
        ).exists()


class IsChurchMember(permissions.BasePermission):
    """
    Allow access to users who are part of the church
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False

        return ChurchRole.objects.filter(
            user=user,
            church=obj.church,
            is_active=True,
        ).exists()
