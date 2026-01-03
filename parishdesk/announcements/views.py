from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema

from .models import Announcement
from .serializers import (
    AnnouncementListSerializer,
    AnnouncementDetailSerializer,
    AnnouncementCreateUpdateSerializer,
)
from .selectors import get_published_announcements, get_all_announcements
from .services import create_announcement, update_announcement
from .permissions import IsStaffOrReadOnly


class AnnouncementViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return get_all_announcements()
        return get_published_announcements()

    def get_serializer_class(self):
        if self.action == "list":
            return AnnouncementListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return AnnouncementCreateUpdateSerializer
        return AnnouncementDetailSerializer

    @extend_schema(tags=["Announcements"])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        announcement = create_announcement(
            created_by=request.user,
            data=serializer.validated_data,
        )

        return Response(
            AnnouncementDetailSerializer(announcement).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(tags=["Announcements"])
    def update(self, request, *args, **kwargs):
        announcement = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        announcement = update_announcement(
            announcement=announcement,
            data=serializer.validated_data,
        )

        return Response(
            AnnouncementDetailSerializer(announcement).data,
            status=status.HTTP_200_OK,
        )
