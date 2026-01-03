from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from core.models import Church, ChurchRole
from teachings.models import Teaching, TeachingCategory


class TeachingsTests(APITestCase):
    def setUp(self):
        # Create users
        self.admin_user = User.objects.create_user(username="admin", password="adminpass")
        self.preacher_user = User.objects.create_user(username="preacher", password="preacherpass")
        self.member_user = User.objects.create_user(username="member", password="memberpass")
        
        # Create church
        self.church = Church.objects.create(name="St Peter", created_by=self.admin_user)
        
        # Assign roles
        ChurchRole.objects.create(user=self.admin_user, church=self.church, role="ADMIN", assigned_by=self.admin_user)
        ChurchRole.objects.create(user=self.preacher_user, church=self.church, role="PREACHER", assigned_by=self.admin_user)
        ChurchRole.objects.create(user=self.member_user, church=self.church, role="MEMBER", assigned_by=self.admin_user)
        
        # Client
        self.client = APIClient()

        # Category
        self.category = TeachingCategory.objects.create(church=self.church, name="Sunday Sermon")
    
    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_create_teaching_as_preacher(self):
        self.authenticate(self.preacher_user)
        data = {
            "title": "Faith & Work",
            "content": "Content of the teaching",
            "church": self.church.id,
            "category_ids": [self.category.id],
        }
        response = self.client.post("/api/v1/teachings/teachings/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teaching.objects.count(), 1)
        self.assertEqual(Teaching.objects.first().preacher, self.preacher_user)

    def test_create_teaching_as_member_forbidden(self):
        self.authenticate(self.member_user)
        data = {
            "title": "Unauthorized Teaching",
            "content": "Should not work",
            "church": self.church.id,
        }
        response = self.client.post("/api/v1/teachings/teachings/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_publish_teaching(self):
        self.authenticate(self.preacher_user)
        teaching = Teaching.objects.create(
            title="Publish Test", content="Content", church=self.church, preacher=self.preacher_user
        )
        response = self.client.post(f"/api/v1/teachings/teachings/{teaching.id}/publish/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        teaching.refresh_from_db()
        self.assertEqual(teaching.status, "PUBLISHED")

    def test_archive_teaching(self):
        self.authenticate(self.preacher_user)
        teaching = Teaching.objects.create(
            title="Archive Test", content="Content", church=self.church, preacher=self.preacher_user
        )
        response = self.client.post(f"/api/v1/teachings/teachings/{teaching.id}/archive/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        teaching.refresh_from_db()
        self.assertEqual(teaching.status, "ARCHIVED")

    def test_bookmark_and_remove(self):
        self.authenticate(self.member_user)
        teaching = Teaching.objects.create(
            title="Bookmark Test", content="Content", church=self.church, preacher=self.preacher_user
        )
        # Bookmark
        response = self.client.post(f"/api/v1/teachings/teachings/{teaching.id}/bookmark/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Remove bookmark
        response = self.client.post(f"/api/v1/teachings/teachings/{teaching.id}/remove_bookmark/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_crud_as_admin(self):
        self.authenticate(self.admin_user)
        # Create category
        data = {"name": "New Category", "church": self.church.id}
        response = self.client.post("/api/v1/teachings/categories/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        category_id = response.data["id"]

        # Update category
        response = self.client.patch(f"/api/v1/teachings/categories/{category_id}/", {"name": "Updated Name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TeachingCategory.objects.get(id=category_id).name, "Updated Name")

        # Delete category
        response = self.client.delete(f"/api/v1/teachings/categories/{category_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TeachingCategory.objects.filter(id=category_id).exists())

    def test_category_crud_forbidden_for_member(self):
        self.authenticate(self.member_user)
        data = {"name": "Forbidden Category", "church": self.church.id}
        response = self.client.post("/api/v1/teachings/categories/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
