from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Church


class Contact(models.Model):
    CONTACT_TYPE_CHOICES = [
        ("MEMBER", "Member"),
        ("VISITOR", "Visitor"),
        ("EXTERNAL", "External"),
    ]

    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name="contacts")
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="contact"
    )

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES)
    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("church", "phone")

    def __str__(self):
        return self.full_name
