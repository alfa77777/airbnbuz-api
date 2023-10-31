from rest_framework import generics
from bookings.models import Booking
from bookings.serializers import BookingCreateSerializer, BookingListSerializer, BookingListUserSerializer
from rest_framework import permissions


class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer

    def get_queryset(self):
        return Booking.objects.select_related('user').all()


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserBookingListView(generics.ListAPIView):
    serializer_class = BookingListUserSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
