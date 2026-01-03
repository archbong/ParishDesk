from django.utils import timezone
from .models import Announcement


def get_published_announcements():
    return Announcement.objects.filter(
        is_published=True,
        published_at__lte=timezone.now(),
    )


def get_all_announcements():
    return Announcement.objects.all()
