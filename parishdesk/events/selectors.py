from .models import Event, Attendance

def list_events_for_church(church):
    return Event.objects.filter(church=church).order_by("-start_time")

def get_event_detail(event_id):
    return Event.objects.get(pk=event_id)

def list_attendance_for_event(event):
    return Attendance.objects.filter(event=event)

def get_attendance_detail(attendance_id):
    return Attendance.objects.get(pk=attendance_id)

