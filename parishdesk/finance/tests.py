from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from core.models import Church, ChurchRole
from finance.models import AccountTransaction

class AccountsTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username="admin", password="adminpass")
        self.treasurer_user = User.objects.create_user(username="treasurer", password="treasurerpass")
        self.member_user = User.objects.create_user(username="member", password="memberpass")
        self.church = Church.objects.create(name="St Peter", created_by=self.admin_user)

        ChurchRole.objects.create(user=self.admin_user, church=self.church, role="ADMIN", assigned_by=self.admin_user)
        ChurchRole.objects.create(user=self.treasurer_user, church=self.church, role="TREASURER", assigned_by=self.admin_user)
        ChurchRole.objects.create(user=self.member_user, church=self.church, role="MEMBER", assigned_by=self.admin_user)

        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_create_transaction_as_admin(self):
        self.authenticate(self.admin_user)
        data = {
            "church": self.church.id,
            "amount": "1000.00",
            "transaction_type": "TITHE",
            "notes": "First tithe"
        }
        response = self.client.post("/api/v1/accounts/transactions/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AccountTransaction.objects.count(), 1)

    def test_create_transaction_as_member_forbidden(self):
        self.authenticate(self.member_user)
        data = {
            "church": self.church.id,
            "amount": "500.00",
            "transaction_type": "OFFERING",
        }
        response = self.client.post("/api/v1/accounts/transactions/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_total_amount_endpoint(self):
        self.authenticate(self.admin_user)
        AccountTransaction.objects.create(
            church=self.church, contributor=self.admin_user, amount=1000, transaction_type="TITHE"
        )
        AccountTransaction.objects.create(
            church=self.church, contributor=self.admin_user, amount=500, transaction_type="OFFERING"
        )
        response = self.client.get(f"/api/v1/accounts/transactions/total/?church={self.church.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total"], 1500)
