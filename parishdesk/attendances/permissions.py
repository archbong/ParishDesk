from rest_framework import permissions
from core.models import ChurchRole


class CanMarkAttendance(permissions.BasePermission):
    """
    Admins, Clergy, or Volunteers can mark attendance
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        church_id = request.data.get("church") or request.query_params.get("church")
        if not church_id:
            return False

        return ChurchRole.objects.filter(
            user=request.user,
            church_id=church_id,
            role__in=["ADMIN", "CLERGY", "VOLUNTEER"],
            is_active=True,
        ).exists()
class CanViewAttendance(permissions.BasePermission):
    """
    Allow access to users who are part of the church
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        church_id = request.query_params.get("church")
        if not church_id:
            return False

        return ChurchRole.objects.filter(
            user=request.user,
            church_id=church_id,
            is_active=True,
        ).exists()