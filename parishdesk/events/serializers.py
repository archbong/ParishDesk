from rest_framework import serializers

from parishdesk.attendances.serializers import AttendanceSerializer
from .models import Event, Attendance, EventReminder, EventMedia

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["created_by", "created_at", "updated_at"]

class EventDetailSerializer(serializers.ModelSerializer):
    attendances = AttendanceSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "church",
            "name",
            "description",
            "event_type",
            "start_time",
            "end_time",
            "created_by",
            "created_at",
            "updated_at",
            "attendances",
        ]
        read_only_fields = ["created_by", "created_at", "updated_at", "attendances"]
        
class EventReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventReminder
        fields = "__all__"
        read_only_fields = ["sent"]

class EventMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventMedia
        fields = "__all__"
        read_only_fields = ["uploaded_at"]