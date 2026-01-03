from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Church
from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer
from .services import mark_attendance, remove_attendance
from .selectors import (
    list_attendance_for_church,
    list_attendance_for_attendable,
    list_attendance_for_user,
)
from .permissions import CanMarkAttendance


class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        church_id = self.request.query_params.get("church")
        attendable_type = self.request.query_params.get("attendable_type")
        attendable_id = self.request.query_params.get("attendable_id")

        if attendable_type and attendable_id:
            return list_attendance_for_attendable(attendable_type, attendable_id)

        if church_id:
            return list_attendance_for_church(church_id)

        return list_attendance_for_user(self.request.user)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated, CanMarkAttendance],
    )
    def mark(self, request):
        church = Church.objects.get(pk=request.data["church"])

        attendance = mark_attendance(
            church=church,
            user=request.user,
            attendable_type=request.data["attendable_type"],
            attendable_id=request.data["attendable_id"],
            notes=request.data.get("notes", ""),
        )

        return Response(
            AttendanceRecordSerializer(attendance).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated, CanMarkAttendance],
    )
    def remove(self, request):
        remove_attendance(
            user=request.user,
            attendable_type=request.data["attendable_type"],
            attendable_id=request.data["attendable_id"],
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
