from django.contrib.auth.models import User
from rest_framework import serializers
from core.models import Church
from .models import (
    Teaching,
    TeachingMedia,
    TeachingCategory,
    TeachingCategoryMap,
    TeachingAudience,
    TeachingBookmark,
)

class TeachingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")

class TeachingMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingMedia
        fields = (
            "id",
            "media_type",
            "file",
            "duration",
            "created_at",
        )
        read_only_fields = ("id", "created_at")

class TeachingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingCategory
        fields = ("id", "name", "slug")

class TeachingReadSerializer(serializers.ModelSerializer):
    preacher = TeachingUserSerializer(read_only=True)
    church = serializers.StringRelatedField()
    media = TeachingMediaSerializer(many=True, read_only=True)
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Teaching
        fields = (
            "id",
            "church",
            "title",
            "description",
            "content",
            "teaching_type",
            "scripture_reference",
            "preacher",
            "status",
            "published_at",
            "media",
            "categories",
            "created_at",
            "updated_at",
        )

    def get_categories(self, obj):
        return [
            TeachingCategorySerializer(link.category).data
            for link in obj.category_links.select_related("category")
        ]

class TeachingWriteSerializer(serializers.ModelSerializer):
    category_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    audience_roles = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Teaching
        fields = (
            "id",
            "church",
            "title",
            "description",
            "content",
            "teaching_type",
            "scripture_reference",
            "status",
            "published_at",
            "category_ids",
            "audience_roles",
        )

    def validate_church(self, church):
        request = self.context["request"]
        if not request.user.is_superuser:
            # Enforce user belongs to this church
            if not request.user.churchrole_set.filter(church=church).exists():
                raise serializers.ValidationError(
                    "You do not belong to this church."
                )
        return church

    def create(self, validated_data):
        category_ids = validated_data.pop("category_ids", [])
        audience_roles = validated_data.pop("audience_roles", [])

        request = self.context["request"]
        teaching = Teaching.objects.create(
            preacher=request.user,
            **validated_data,
        )

        # Categories
        if category_ids:
            categories = TeachingCategory.objects.filter(id__in=category_ids)
            TeachingCategoryMap.objects.bulk_create(
                [
                    TeachingCategoryMap(teaching=teaching, category=cat)
                    for cat in categories
                ]
            )

        # Audience roles
        if audience_roles:
            TeachingAudience.objects.bulk_create(
                [
                    TeachingAudience(teaching=teaching, role=role)
                    for role in set(audience_roles)
                ]
            )

        return teaching

    def update(self, instance, validated_data):
        category_ids = validated_data.pop("category_ids", None)
        audience_roles = validated_data.pop("audience_roles", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if category_ids is not None:
            TeachingCategoryMap.objects.filter(teaching=instance).delete()
            categories = TeachingCategory.objects.filter(id__in=category_ids)
            TeachingCategoryMap.objects.bulk_create(
                [
                    TeachingCategoryMap(teaching=instance, category=cat)
                    for cat in categories
                ]
            )

        if audience_roles is not None:
            TeachingAudience.objects.filter(teaching=instance).delete()
            TeachingAudience.objects.bulk_create(
                [
                    TeachingAudience(teaching=instance, role=role)
                    for role in set(audience_roles)
                ]
            )

        return instance
