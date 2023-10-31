from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import APIException

from bookings.models import Booking
from users.serializers import UserSerializer


class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("id", "date_in", "date_out", "total_price", "room", "user")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["room"] = instance.room.title
        return data


class BookingListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("id", "date_in", "date_out", "total_price", "room")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["room"] = instance.room.title
        return data


class BookingForPaymentSerializer(serializers.ModelSerializer):
    room_slug = serializers.CharField(write_only=True, max_length=255)
    price = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ("id", "date_in", "date_out", "guests", "price", "room_slug")


class BadRequestException(APIException):
    status_code = 400
    default_detail = "Bad request."


class BookingCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ("id", "date_in", "date_out", "guests", "total_price", "room", "user")

    def create(self, validated_data):
        user = self.context["request"].user
        room = validated_data.get("room")
        validated_data["user"] = user
        if validated_data.get("guests") > room.guests:
            raise BadRequestException(detail="Guests must be smaller than Room Guests")

        if validated_data.get("date_in") >= validated_data.get("date_out"):
            raise BadRequestException(detail="Date out must be bigger than Date in")

        overlapping_bookings = Booking.objects.filter(room=room).filter(
            models.Q(date_in__lte=validated_data["date_in"], date_out__gt=validated_data["date_in"])
            | models.Q(date_in__lt=validated_data["date_out"], date_out__gte=validated_data["date_out"])
            | models.Q(date_in__gte=validated_data["date_in"], date_out__lte=validated_data["date_out"])
        )

        if overlapping_bookings.exists():
            raise BadRequestException(detail="The room is already booked for the selected dates.")

        try:
            booking = super().create(validated_data)
        except serializers.ValidationError as e:
            raise BadRequestException(detail=e.detail)

        return booking
