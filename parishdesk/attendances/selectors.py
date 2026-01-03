from .models import AttendanceRecord


def list_attendance_for_church(church):
    return AttendanceRecord.objects.filter(church=church)


def list_attendance_for_attendable(attendable_type, attendable_id):
    return AttendanceRecord.objects.filter(
        attendable_type=attendable_type,
        attendable_id=attendable_id,
    )


def list_attendance_for_user(user):
    return AttendanceRecord.objects.filter(user=user)
