from .models import Event, Attendance, EventReminder, EventMedia

def create_event(church, created_by, **data):
    return Event.objects.create(church=church, created_by=created_by, **data)

def update_event(event, **data):
    for key, value in data.items():
        setattr(event, key, value)
    event.save()
    return event

def record_event_reminder(event, sent=False):
    return EventReminder.objects.create(event=event, sent=sent)

def add_event_media(event, media_type, file):
    return EventMedia.objects.create(event=event, media_type=media_type, file=file)