from .models import ChurchRole, Church
from django.contrib.auth.models import User

def list_churches():
    return Church.objects.all().order_by("name")

def get_church_by_id(church_id):
    return Church.objects.filter(id=church_id).first()

def get_user_church_role(user: User):
    return ChurchRole.objects.filter(user=user, is_active=True).select_related("church")
