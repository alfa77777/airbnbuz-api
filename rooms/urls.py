from django.urls import path

from rooms.views import FacilitiesView, ReviewsInRoomView, RoomDetailView, RoomListView, ReviewCreateView

urlpatterns = [
    path("", RoomListView.as_view(), name="rooms-list"),
    path("facilities/", FacilitiesView.as_view(), name="facilities"),
    path("<str:slug>/", RoomDetailView.as_view(), name="rooms-detail"),
    path("<str:slug>/reviews", ReviewsInRoomView.as_view(), name="reviews"),
    path("<str:slug>/reviews/create", ReviewCreateView.as_view(), name="reviews-create"),
]
