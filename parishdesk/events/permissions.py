from rest_framework import permissions
from core.models import ChurchRole

class IsChurchAdminOrCreator(permissions.BasePermission):
    """
    Allow only church admin or the creator of the event to modify
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.created_by == user:
            return True

        return ChurchRole.objects.filter(
            user=user,
            church=obj.church,
            role="ADMIN",
            is_active=True
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