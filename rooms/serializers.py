from django.db.models import Avg
from rest_framework import serializers

from rooms.models import Facility, Review, Room, RoomPhotos, Service
from users.serializers import UserSerializer


class RoomPhotosSerializers(serializers.ModelSerializer):
    class Meta:
        model = RoomPhotos
        fields = ("photo",)


class ServiceSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ["name", "count", "icon"]

    def get_count(self, obj):
        return obj.services.count()


class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["name", "icon"]


class RoomListSerializers(serializers.ModelSerializer):
    photos = RoomPhotosSerializers(many=True)
    reviews_info = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ("id", "title", "slug", "price", "region", "reviews_info", "photos")

    def get_reviews_info(self, obj):
        return obj.get_reviews_info()


class RoomDetailSerializers(serializers.ModelSerializer):
    photos = RoomPhotosSerializers(many=True)

    class Meta:
        model = Room
        fields = (
            "id",
            "title",
            "description",
            "guests",
            "price",
            "region",
            "address",
            "is_active",
            "location",
            "user",
            "photos",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["services"] = ServiceSerializer(instance.service.all(), many=True).data
        data["facilities"] = FacilitiesSerializer(instance.facilities.all(), many=True).data
        reviews = instance.reviews.all()
        count = reviews.count()

        average_rating = reviews.aggregate(average=Avg("rating"))["average"] or 0

        positive_count = reviews.filter(rating__gte=4).count()
        neutral_count = reviews.filter(rating=3).count()
        negative_count = reviews.filter(rating__lte=2).count()

        data["reviews_data"] = {
            "count": count,
            "average": average_rating,
            "positive": positive_count,
            "neutral": neutral_count,
            "negative": negative_count,
        }
        return data


class RoomSerializersForCreate(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ("title", "description", "price", "region", "address", "is_active", "guests", "lat", "lng", "user")

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)


class FacilitiesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ("id", "name", "icon")


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "comment", "rating", "parent", "user", "created_at")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = instance.user.first_name
        return data


class ReviewSerializerCreate(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "comment", "rating", "parent", "user", "created_at")

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        review = super().create(validated_data)
        return review
