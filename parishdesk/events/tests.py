from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from core.models import Church, ChurchRole
from events.models import Event, Attendance

class EventsTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username="admin", password="adminpass")
        self.member_user = User.objects.create_user(username="member", password="memberpass")
        self.church = Church.objects.create(name="St Peter", created_by=self.admin_user)
        ChurchRole.objects.create(user=self.admin_user, church=self.church, role="ADMIN", assigned_by=self.admin_user)
        ChurchRole.objects.create(user=self.member_user, church=self.church, role="MEMBER", assigned_by=self.admin_user)

        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_create_event_as_admin(self):
        self.authenticate(self.admin_user)
        data = {
            "name": "Sunday Service",
            "church": self.church.id,
            "event_type": "SERVICE",
            "start_time": "2025-01-05T09:00:00Z",
            "end_time": "2025-01-05T11:00:00Z"
        }
        response = self.client.post("/api/v1/events/events/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)

    def test_check_in_attendance(self):
        self.authenticate(self.member_user)
        event = Event.objects.create(
            name="Test Event",
            church=self.church,
            start_time="2025-01-05T09:00:00Z",
            end_time="2025-01-05T11:00:00Z",
            created_by=self.admin_user
        )
        response = self.client.post("/api/v1/events/attendances/check_in/", {"event": event.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 1)
        self.assertEqual(Attendance.objects.first().attendee, self.member_user)
