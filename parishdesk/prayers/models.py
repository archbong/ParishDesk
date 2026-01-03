from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Church


class PrayerRequest(models.Model):
    VISIBILITY_CHOICES = [
        ("PRIVATE", "Private"),
        ("LEADERS", "Leaders"),
        ("PUBLIC", "Public"),
    ]

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("ANSWERED", "Answered"),
    ]

    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name="prayer_requests")
    requested_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    is_anonymous = models.BooleanField(default=False)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
class PrayerResponse(models.Model):
    prayer_request = models.ForeignKey(
        PrayerRequest, on_delete=models.CASCADE, related_name="responses"
    )
    responded_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )

    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Response to {self.prayer_request.title} by {self.responded_by.username if self.responded_by else 'Anonymous'}"

