from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Church


class Asset(models.Model):
    CONDITION_CHOICES = [
        ("NEW", "New"),
        ("GOOD", "Good"),
        ("FAIR", "Fair"),
        ("DAMAGED", "Damaged"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("RETIRED", "Retired"),
        ("LOST", "Lost"),
    ]

    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name="assets")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    asset_tag = models.CharField(max_length=100, unique=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")

    assigned_to = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_assets"
    )

    acquired_at = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.asset_tag})"
