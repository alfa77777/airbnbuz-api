import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestBooking:
    def test_booking_list(self, client):
        url = reverse("bookings-list")
        response = client.get(url)
        assert response.status_code == 200

    def test_booking_create(self, client):
        url = reverse("bookings-create")
        response = client.get(url)
        assert response.status_code == 200
