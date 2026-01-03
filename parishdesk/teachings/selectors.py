from django.db.models import Q
from django.contrib.auth.models import User

from core.models import Church
from .models import (
    Teaching,
    TeachingCategory,
    TeachingBookmark,
    TeachingViewLog,
)


def list_teachings_for_church(
    *,
    church: Church,
    user: User | None = None,
    include_drafts: bool = False,
):
    """
    List teachings visible to a user in a church.
    - Anonymous users: published only
    - Authenticated users: role-based visibility
    """

    qs = Teaching.objects.filter(church=church)

    if not include_drafts:
        qs = qs.filter(status=Teaching.status.PUBLISHED)

    if user and user.is_authenticated:
        # If teaching has audience restrictions, user must match one
        user_roles = set(
            user.church_roles.filter(
                church=church, is_active=True
            ).values_list("role", flat=True)
        )

        qs = qs.filter(
            Q(audiences__isnull=True)
            | Q(audiences__role__in=user_roles)
        ).distinct()

    return qs.select_related(
        "church", "preacher"
    ).prefetch_related(
        "media",
        "category_links__category",
    )


def get_teaching_detail(
    *,
    teaching_id,
    church: Church,
):
    return (
        Teaching.objects.filter(id=teaching_id, church=church)
        .select_related("church", "preacher")
        .prefetch_related(
            "media",
            "category_links__category",
            "audiences",
        )
        .first()
    )


def list_categories_for_church(church: Church):
    return TeachingCategory.objects.filter(church=church).order_by("name")


def list_user_bookmarks(user: User):
    return (
        TeachingBookmark.objects.filter(user=user)
        .select_related("teaching__church", "teaching__preacher")
        .prefetch_related("teaching__media")
    )


def teaching_is_bookmarked(*, teaching, user: User) -> bool:
    return TeachingBookmark.objects.filter(
        teaching=teaching, user=user
    ).exists()
