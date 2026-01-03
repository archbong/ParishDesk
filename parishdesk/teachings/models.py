import uuid
from django.db import models
from django.contrib.auth.models import User
from core.models import Church


class TeachingType(models.TextChoices):
    SERMON = "SERMON", "Sermon"
    BIBLE_STUDY = "BIBLE_STUDY", "Bible Study"
    CLASS = "CLASS", "Class"
    DEVOTIONAL = "DEVOTIONAL", "Devotional"


class TeachingStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    ARCHIVED = "ARCHIVED", "Archived"


class Teaching(models.Model):
    """
    Core teaching entity (sermons, lessons, studies).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    church = models.ForeignKey(
        Church, on_delete=models.CASCADE, related_name="teachings"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField()

    teaching_type = models.CharField(
        max_length=20, choices=TeachingType.choices
    )

    scripture_reference = models.CharField(max_length=255, blank=True)

    preacher = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="teachings"
    )

    status = models.CharField(
        max_length=20, choices=TeachingStatus.choices, default=TeachingStatus.DRAFT
    )

    published_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["church", "status"]),
            models.Index(fields=["church", "teaching_type"]),
        ]
        unique_together = ("church", "title")

    def __str__(self):
        return f"{self.title} ({self.church.name})"
    
    def get_preacher_full_name(self):
        return self.preacher.get_full_name() if self.preacher else "Unknown Preacher"
    
class MediaType(models.TextChoices):
    AUDIO = "AUDIO", "Audio"
    VIDEO = "VIDEO", "Video"
    PDF = "PDF", "PDF"
    IMAGE = "IMAGE", "Image"


class TeachingMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teaching = models.ForeignKey(
        Teaching, on_delete=models.CASCADE, related_name="media"
    )

    media_type = models.CharField(
        max_length=10, choices=MediaType.choices
    )

    file = models.FileField(upload_to="teachings/media/")
    duration = models.PositiveIntegerField(
        null=True, blank=True, help_text="Duration in seconds"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["media_type"]),
        ]

    def __str__(self):
        return f"{self.media_type} for {self.teaching.title}"

class TeachingCategory(models.Model):
    church = models.ForeignKey(
        Church, on_delete=models.CASCADE, related_name="teaching_categories"
    )

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("church", "slug")
        ordering = ["name"]

    def __str__(self):
        return self.name

class TeachingCategoryMap(models.Model):
    teaching = models.ForeignKey(
        Teaching, on_delete=models.CASCADE, related_name="category_links"
    )
    category = models.ForeignKey(
        TeachingCategory, on_delete=models.CASCADE, related_name="teaching_links"
    )

    class Meta:
        unique_together = ("teaching", "category")

class TeachingAudience(models.Model):
    teaching = models.ForeignKey(
        Teaching, on_delete=models.CASCADE, related_name="audiences"
    )

    role = models.CharField(
        max_length=50,
        help_text="Church role allowed to view this teaching",
    )

    class Meta:
        unique_together = ("teaching", "role")

    def __str__(self):
        return f"{self.role} audience for {self.teaching.title}"

class TeachingBookmark(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="teaching_bookmarks"
    )
    teaching = models.ForeignKey(
        Teaching, on_delete=models.CASCADE, related_name="bookmarks"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "teaching")

    def __str__(self):
        return f"{self.user.username} bookmarked {self.teaching.title}"

class TeachingViewLog(models.Model):
    teaching = models.ForeignKey(
        Teaching, on_delete=models.CASCADE, related_name="view_logs"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    viewed_at = models.DateTimeField(auto_now_add=True)
    device = models.CharField(max_length=50, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["teaching", "viewed_at"]),
        ]
