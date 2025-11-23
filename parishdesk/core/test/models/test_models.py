import pytest
from django.contrib.auth.models import User
from core.models import Church, ChurchRole


@pytest.mark.django_db
def test_create_church_and_role():
    u = User.objects.create(username="John", password="Password@123")
    c = Church.objects.create(name="St Pauls", created_by=u)
    role = ChurchRole.objects.create(user=u, church=u, role="Admin", created_by=u)

    assert c.name == "St Pauls"
    assert role.role == "Admin"
