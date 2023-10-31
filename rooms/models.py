from django.db import models
from django.db.models import Avg
from django.utils.text import slugify

from common.models import BaseModel, Region


class Room(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    address = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()
    is_active = models.BooleanField(default=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True, related_name="rooms")
    slug = models.CharField(max_length=255, null=True, blank=True)
    guests = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    facilities = models.ManyToManyField("Facility", blank=True, related_name="facilities")
    service = models.ManyToManyField("Service", blank=True, related_name="services")

    def __str__(self):
        return self.title

    @property
    def location(self):
        location = {"lat": self.lat, "lng": self.lng}
        return location  # noqa

    def get_reviews_info(self):
        reviews = self.reviews.all()
        count = reviews.count()
        average = (
            reviews.aggregate(
                average=Avg(
                    models.Case(
                        models.When(rating="1", then=1),
                        models.When(rating="2", then=2),
                        models.When(rating="3", then=3),
                        models.When(rating="4", then=4),
                        models.When(rating="5", then=5),
                        output_field=models.IntegerField(),
                    )
                )
            )["average"]
            or 0
        )
        return {"count": count, "average": average}

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title.lower())
        return super().save(force_insert, force_update, using, update_fields)


class RoomPhotos(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="photos")
    photo = models.ImageField(upload_to="images/")
    position = models.SmallIntegerField(default=1)


class Service(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.name


class Facility(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True)
    icon = models.ImageField(upload_to="images/", null=True, blank=True)
    position = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name.lower())
        return super().save(force_insert, force_update, using, update_fields)


RATING_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]


class Review(BaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name="reviews", on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="child_comments")
    comment = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=1)

    @property
    def average_rating(self):
        ratings_sum = self.room.reviews.aggregate(total=models.Sum("ratings"))["total"]
        ratings_count = self.room.reviews.count()

        if ratings_sum is None or ratings_count == 0:
            return 0

        return ratings_sum / ratings_count
