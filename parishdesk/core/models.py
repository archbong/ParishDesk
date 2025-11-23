import uuid
from django.conf import settings
from django.db import models

from django.utils import timezone



# Roles
ROLE_CHOICES = [
    ("ADMIN", "Admin"),
    ("CLERGY", "Clergy"),
    ("TREASURER", "Treasurer"),
    ("VOLUNTEER", "Volunteer"),
    ("INTERN", "Intern"),
]
# Create your models here.
class Church(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(blank=True)
    district = models.CharField(max_length=255, unique=True, blank=True)
    phone = models.CharField(max_length=13, unique=True, blank=True)
    email = models.EmailField(blank=True)
    current_timezone = models.CharField(max_length=64, default="UTC")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="created_churches")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Church"

    def __str__(self) -> str:
        return f"{self.name}"

class UserProfile(models.Model):
    """
    One-to-one extension of default User for profile fields
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13, unique=True)
    avatar = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "Profile"

    def __str__(self) -> str:
        return f"{self.get_fullname()}"


class ChurchRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="church_roles")
    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name="roles")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name="assigned_roles")
    assigned_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "church", "role")
        indexes = [
            models.Index(fields=["church", "role"]),
            models.Index(fields=["user", "role"]),
        ]

        def __str__(self):
            return f"{self.user.username} - {self.role}@{self.church.name}"
