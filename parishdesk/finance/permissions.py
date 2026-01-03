from rest_framework import permissions
from core.models import ChurchRole

class IsChurchAdminOrTreasurer(permissions.BasePermission):
    """
    Allow only church admins or treasurers to create/update transactions
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        church_id = request.data.get("church") or request.query_params.get("church")
        if not church_id:
            return False
        from core.models import Church
        from django.core.exceptions import ObjectDoesNotExist
        try:
            from core.models import ChurchRole
            return ChurchRole.objects.filter(
                user=user,
                church__id=church_id,
                role__in=["ADMIN", "TREASURER"],
                is_active=True
            ).exists()
        except ObjectDoesNotExist:
            return False

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