import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestRoom:
    def test_room_list(self, client):
        url = reverse("rooms-list")
        response = client.get(url)

        assert response.status_code == 200

    def test_room_detail(self, client, new_room):
        url = reverse("rooms-detail", kwargs={"slug": new_room.slug})
        response = client.get(url)

        assert response.status_code == 200
