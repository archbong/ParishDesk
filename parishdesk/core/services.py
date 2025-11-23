from django.core.exceptions import PermissionDenied
from .models import Church, ChurchRole
from django.contrib.auth.models import User


def create_church(dict: dict, created_by: User):
    church = Church.objects.create(created_by=created_by)
    # Give creator admin role
    Church.objects.create(user=created_by, church=church, role="Admin", assigned_by=created_by)
    return church

def assign_role(user, church, role, assigned_by):
    if role not in dict(ChurchRole._meta.get_field("role").choices):
        raise ValueError("Invalid role.")

    # Simple check: only Admin of church or SuperAdmin can assign
    if not (assigned_by.is_superuser or ChurchRole.objects.filter(user=assigned_by, church=church, role="Admin", is_active=True).exists()):
       raise PermissionDenied("You are not allowed to assigned roles for this church")
    return ChurchRole.objects.create(user=user, church=church, role=role, assigned_by=assigned_by)
