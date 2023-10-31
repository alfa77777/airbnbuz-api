from django.urls import path

from bookings.views import BookingCreateView, BookingListView,UserBookingListView


urlpatterns = [
    path("list/", BookingListView.as_view(), name="bookings-list"),
    path("create/", BookingCreateView.as_view(), name="bookings-create"),
    path("user-booking-list/", UserBookingListView.as_view(), name="user-bookings-list"),
]
