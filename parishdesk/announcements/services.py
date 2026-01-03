from django.utils import timezone
from .models import Announcement


def create_announcement(*, created_by, data):
    is_published = data.get("is_published", False)

    announcement = Announcement.objects.create(
        title=data["title"],
        body=data["body"],
        is_published=is_published,
        published_at=timezone.now() if is_published else None,
        created_by=created_by,
    )

    return announcement


def update_announcement(*, announcement, data):
    for field in ["title", "body", "is_published"]:
        if field in data:
            setattr(announcement, field, data[field])

    if data.get("is_published") and not announcement.published_at:
        announcement.published_at = timezone.now()

    announcement.save()
    return announcement
