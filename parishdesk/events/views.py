from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Event, Attendance
from .serializers import EventSerializer, AttendanceSerializer
from .services import create_event, check_in_attendance, update_event
from .selectors import list_events_for_church, list_attendance_for_event
from .permissions import IsChurchAdminOrCreator

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsChurchAdminOrCreator]

    def get_queryset(self):
        church_id = self.request.query_params.get("church")
        if not church_id:
            return Event.objects.none()
        from core.models import Church
        church = Church.objects.get(pk=church_id)
        return list_events_for_church(church)

    def perform_create(self, serializer):
        church_id = self.request.data.get("church")
        from core.models import Church
        church = Church.objects.get(pk=church_id)
        serializer.instance = create_event(church=church, created_by=self.request.user, **serializer.validated_data)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.request.query_params.get("event")
        if not event_id:
            return Attendance.objects.none()
        from .models import Event
        event = Event.objects.get(pk=event_id)
        return list_attendance_for_event(event)

    @action(detail=False, methods=["post"])
    def check_in(self, request):
        event_id = request.data.get("event")
        from .models import Event
        event = Event.objects.get(pk=event_id)
        attendance = check_in_attendance(event=event, user=request.user, notes=request.data.get("notes", ""))
        return Response(AttendanceSerializer(attendance).data, status=status.HTTP_201_CREATED)

