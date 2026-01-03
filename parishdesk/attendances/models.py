from django.db import models
from django.contrib.auth.models import User
from core.models import Church


class Attendance(models.Model):
    ATTENDABLE_TYPES = [
        ("EVENT", "Event"),
        ("SERVICE", "Sunday Service"),
        ("TEACHING", "Teaching"),
        ("OTHER", "Other"),
    ]

    church = models.ForeignKey(
        Church,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    attendable_type = models.CharField(max_length=20, choices=ATTENDABLE_TYPES)
    attendable_id = models.PositiveIntegerField()

    attended_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("user", "attendable_type", "attendable_id")
        ordering = ["-attended_at"]

    def __str__(self):
        return f"{self.user.username} attended {self.attendable_type}({self.attendable_id})"
