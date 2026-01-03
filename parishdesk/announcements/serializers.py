from rest_framework import serializers
from .models import Announcement


class AnnouncementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            "id",
            "title",
            "is_published",
            "published_at",
            "created_at",
        ]


class AnnouncementDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Announcement
        fields = [
            "id",
            "title",
            "body",
            "is_published",
            "published_at",
            "created_by",
            "created_at",
            "updated_at",
        ]


class AnnouncementCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            "title",
            "body",
            "is_published",
            "published_at",
        ]
