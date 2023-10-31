from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from custom_permission import IsOwnerOrReadOnly
from rooms.filters import RoomFilter
from rooms.models import Facility, Review, Room
from rooms.serializers import (
    FacilitiesSerializers,
    ReviewSerializers,
    RoomDetailSerializers,
    RoomListSerializers,
    RoomSerializersForCreate, ReviewSerializerCreate,
)
from utils.pagination import WithTotalPagesCountPagination


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RoomFilter
    serializer_class = RoomListSerializers
    pagination_class = WithTotalPagesCountPagination


class RoomDetailView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializers
    lookup_field = "slug"
    permission_classes = [IsOwnerOrReadOnly]


class RoomCreateView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializersForCreate
    permissions_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FacilitiesView(generics.ListAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitiesSerializers
    pagination_class = WithTotalPagesCountPagination


class ReviewsInRoomView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    pagination_class = WithTotalPagesCountPagination

    def get_queryset(self):
        room_slug = self.kwargs.get("slug")
        reviews = Review.objects.filter(room__slug=room_slug)
        return reviews.all()


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializerCreate
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        room_slug = self.kwargs['slug']
        room = Room.objects.get(slug=room_slug)
        user = self.request.user

        serializer.save(user=user, room=room)
