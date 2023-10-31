from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from rooms.models import Room


class Booking(BaseModel):
    class ApplyStatus(models.Choices):
        UNPAID = "unpaid"
        PAID = "paid"

    date_in = models.DateField()
    date_out = models.DateField()
    guests = models.PositiveIntegerField()
    total_price = models.SmallIntegerField(blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="bookings")
    status = models.CharField(max_length=20, choices=ApplyStatus.choices, default=ApplyStatus.UNPAID)

    def __str__(self):
        return f"{self.room.title} - {self.user}"

    def duration(self):
        return (self.date_out - self.date_in).days

    @property
    def calculate_total_price(self):
        return self.duration() * self.room.price

    def clean(self):
        # Check for overlapping bookings for the same room
        conflicting_bookings = Booking.objects.filter(
            room=self.room,
            date_in__lt=self.date_out,
            date_out__gt=self.date_in
        ).exclude(pk=self.pk)

        if conflicting_bookings.exists():
            raise ValidationError("This room is already booked for the selected dates.")

        # Check date_in and date_out range
        if self.date_in >= self.date_out:
            raise ValidationError({"date_out": ValidationError("Date out must be bigger than Date in")})

    # Your other methods and properties here
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.date_in >= self.date_out:
            raise ValidationError({"date_out": ValidationError("Date out  must be bigger than Date in")})
        self.total_price = self.calculate_total_price

        if self.guests > self.room.guests:
            raise ValidationError({"guests": ValidationError("Guests count must be same or small ")})
        return super().save(force_insert, force_update, using, update_fields)
