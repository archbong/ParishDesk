from .models import AttendanceRecord


def mark_attendance(
    *,
    church,
    user,
    attendable_type,
    attendable_id,
    notes=""
):
    attendance, created = AttendanceRecord.objects.get_or_create(
        church=church,
        user=user,
        attendable_type=attendable_type,
        attendable_id=attendable_id,
        defaults={"notes": notes},
    )

    if not created and notes:
        attendance.notes = notes
        attendance.save()

    return attendance


def remove_attendance(user, attendable_type, attendable_id):
    AttendanceRecord.objects.filter(
        user=user,
        attendable_type=attendable_type,
        attendable_id=attendable_id,
    ).delete()
def get_attendance_records(
    *,
    church,
    attendable_type,
    attendable_id,
):
    records = AttendanceRecord.objects.filter(
        church=church,
        attendable_type=attendable_type,
        attendable_id=attendable_id,
    ).select_related("user")

    return records  