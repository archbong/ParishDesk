from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.models import Church
from .models import Teaching, TeachingCategory
from .serializers import (
    TeachingSerializer,
    TeachingCategorySerializer,
)
from .permissions import IsPreacherOrAdmin, IsChurchMember
from .services import (
    create_teaching,
    update_teaching,
    publish_teaching,
    archive_teaching,
    record_teaching_view,
    bookmark_teaching,
    remove_bookmark,
)
from .selectors import (
    list_teachings_for_church,
    get_teaching_detail,
    list_categories_for_church,
    teaching_is_bookmarked,
)


class TeachingViewSet(viewsets.ModelViewSet):
    """
    CRUD for Teachings
    """
    queryset = Teaching.objects.all()
    serializer_class = TeachingSerializer
    permission_classes = [IsPreacherOrAdmin]

    def get_queryset(self):
        user = self.request.user
        church_id = self.request.query_params.get("church")
        if not church_id:
            return Teaching.objects.none()

        church = Church.objects.get(id=church_id)
        return list_teachings_for_church(church=church, user=user)

    def perform_create(self, serializer):
        user = self.request.user
        church_id = self.request.data.get("church")
        church = Church.objects.get(id=church_id)

        teaching = create_teaching(
            church=church,
            preacher=user,
            title=serializer.validated_data.get("title"),
            content=serializer.validated_data.get("content"),
            teaching_type=serializer.validated_data.get("teaching_type"),
            description=serializer.validated_data.get("description", ""),
            scripture_reference=serializer.validated_data.get("scripture_reference", ""),
            status=serializer.validated_data.get("status", "DRAFT"),
            category_ids=self.request.data.get("category_ids", []),
            audience_roles=self.request.data.get("audience_roles", []),
        )
        serializer.instance = teaching

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        teaching = self.get_object()
        publish_teaching(teaching=teaching)
        return Response({"status": "published"})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def archive(self, request, pk=None):
        teaching = self.get_object()
        archive_teaching(teaching=teaching)
        return Response({"status": "archived"})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):
        teaching = self.get_object()
        bookmark_teaching(teaching=teaching, user=request.user)
        return Response({"status": "bookmarked"})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def remove_bookmark(self, request, pk=None):
        teaching = self.get_object()
        remove_bookmark(teaching=teaching, user=request.user)
        return Response({"status": "bookmark removed"})


class TeachingCategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD for teaching categories
    """
    queryset = TeachingCategory.objects.all()
    serializer_class = TeachingCategorySerializer
    permission_classes = [IsPreacherOrAdmin]

    def get_queryset(self):
        church_id = self.request.query_params.get("church")
        if not church_id:
            return TeachingCategory.objects.none()
        church = Church.objects.get(id=church_id)
        return list_categories_for_church(church)
