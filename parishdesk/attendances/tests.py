from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from core.models import Church, ChurchRole
from .models import AttendanceRecord


class AttendanceTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass")
        self.member = User.objects.create_user(username="member", password="pass")

        self.church = Church.objects.create(name="St Peter", created_by=self.admin)

        ChurchRole.objects.create(
            user=self.admin,
            church=self.church,
            role="ADMIN",
            assigned_by=self.admin,
        )

        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_mark_attendance(self):
        self.authenticate(self.admin)
        data = {
            "church": self.church.id,
            "attendable_type": "EVENT",
            "attendable_id": 1,
        }

        response = self.client.post("/api/v1/attendance/records/mark/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AttendanceRecord.objects.count(), 1)

    def test_no_duplicate_attendance(self):
        self.authenticate(self.admin)
        data = {
            "church": self.church.id,
            "attendable_type": "SERVICE",
            "attendable_id": 1,
        }

        self.client.post("/api/v1/attendance/records/mark/", data, format="json")
        self.client.post("/api/v1/attendance/records/mark/", data, format="json")

        self.assertEqual(AttendanceRecord.objects.count(), 1)
