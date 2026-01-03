from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Church, ChurchRole


class ChurchModelTest(TestCase):

    def test_create_church_and_role(self):
        u = User.objects.create(username="John", password="Password@123")
        c = Church.objects.create(name="St Pauls", created_by=u)
        role = ChurchRole.objects.create(user=u, church=c, role="Admin", assigned_by=u)

        self.assertEqual(c.name, "St Pauls")
        self.assertEqual(role.role, "Admin")
