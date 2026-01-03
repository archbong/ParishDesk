from django.db import models
from django.contrib.auth.models import User
from core.models import Church

class Event(models.Model):
    EVENT_TYPES = [
        ("SERVICE", "Service"),
        ("MEETING", "Meeting"),
        ("PROGRAM", "Program"),
        ("BIRTHDAY", "Birthday"),
        ("OTHER", "Other"),
    ]

    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default="OTHER")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_events")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_time"]

    def __str__(self):
        return f"{self.name} ({self.church.name})"

class EventReminder(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reminders")
    remind_at = models.DateTimeField()
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["remind_at"]

    def __str__(self):
        return f"Reminder for {self.event.name} at {self.remind_at}"

class EventMedia(models.Model):
    MEDIA_TYPES = [
        ("IMAGE", "Image"),
        ("VIDEO", "Video"),
        ("AUDIO", "Audio"),
        ("DOCUMENT", "Document"),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="media")
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    file = models.FileField(upload_to="event_media/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.media_type} for {self.event.name}"