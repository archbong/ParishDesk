from rest_framework.permissions import BasePermission
from .models import ChurchRole
from fnmatch import filter


class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return bool(request.user and request.user.is_superuser)

class IsChurchAdmin(BasePermission):
    """
    Allow access only to admins of selected church
    Views should call church_ids in kwargs or pass church is request.data
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        church_id = request.data.get("church") or view.kwargs.get("church_id") or request.query_params.get("church")
        if user.is_superuser:
            return True
        if not church_id:
            return False
        return ChurchRole.object.filter(user=user, church_id=church_id, role="Admin", is_active=True).exist()

class HasChurchRole(BasePermission):
    """
    Generic permission: View should set `required_roles` attribute (list of role strings)
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        required = getattr(view, "required_roles", None)
        church_id = request.data.get("church") or request.query_params.get("church") or view.kwargs.get("church_id")
        if user.is_superuser:
            return True
        if not required:
            return True
        if not church_id:
            return False
        return ChurchRole.objects.filter(user=user, church_id=church_id, role__in=required, is_active=True).exist()
# Usage: set required_roles = ["CLERGY", "TREASURER"] on ViewSets.
