from django.utils import timezone
from django.contrib.auth.models import User

from core.models import Church
from .models import (
    Teaching,
    TeachingCategory,
    TeachingCategoryMap,
    TeachingAudience,
    TeachingBookmark,
    TeachingViewLog,
)


def create_teaching(
    *,
    church: Church,
    preacher: User,
    title: str,
    content: str,
    teaching_type: str,
    description: str = "",
    scripture_reference: str = "",
    status: str = "DRAFT",
    published_at=None,
    category_ids: list[int] | None = None,
    audience_roles: list[str] | None = None,
) -> Teaching:
    """
    Create a teaching with categories and audience rules.
    """

    teaching = Teaching.objects.create(
        church=church,
        preacher=preacher,
        title=title,
        description=description,
        content=content,
        teaching_type=teaching_type,
        scripture_reference=scripture_reference,
        status=status,
        published_at=published_at,
    )

    if category_ids:
        categories = TeachingCategory.objects.filter(
            id__in=category_ids, church=church
        )
        TeachingCategoryMap.objects.bulk_create(
            [
                TeachingCategoryMap(teaching=teaching, category=cat)
                for cat in categories
            ]
        )

    if audience_roles:
        TeachingAudience.objects.bulk_create(
            [
                TeachingAudience(teaching=teaching, role=role)
                for role in set(audience_roles)
            ]
        )

    return teaching


def publish_teaching(*, teaching: Teaching):
    teaching.status = "PUBLISHED"
    teaching.published_at = timezone.now()
    teaching.save(update_fields=["status", "published_at"])


def archive_teaching(*, teaching: Teaching):
    teaching.status = "ARCHIVED"
    teaching.save(update_fields=["status"])


def update_teaching(
    *,
    teaching: Teaching,
    data: dict,
    category_ids: list[int] | None = None,
    audience_roles: list[str] | None = None,
) -> Teaching:
    for field, value in data.items():
        setattr(teaching, field, value)

    teaching.save()

    if category_ids is not None:
        TeachingCategoryMap.objects.filter(teaching=teaching).delete()
        categories = TeachingCategory.objects.filter(
            id__in=category_ids, church=teaching.church
        )
        TeachingCategoryMap.objects.bulk_create(
            [
                TeachingCategoryMap(teaching=teaching, category=cat)
                for cat in categories
            ]
        )

    if audience_roles is not None:
        TeachingAudience.objects.filter(teaching=teaching).delete()
        TeachingAudience.objects.bulk_create(
            [
                TeachingAudience(teaching=teaching, role=role)
                for role in set(audience_roles)
            ]
        )

    return teaching


def record_teaching_view(
    *,
    teaching: Teaching,
    user: User | None = None,
    device: str = "",
):
    TeachingViewLog.objects.create(
        teaching=teaching,
        user=user,
        device=device,
    )


def bookmark_teaching(*, teaching: Teaching, user: User):
    TeachingBookmark.objects.get_or_create(
        teaching=teaching, user=user
    )


def remove_bookmark(*, teaching: Teaching, user: User):
    TeachingBookmark.objects.filter(
        teaching=teaching, user=user
    ).delete()
