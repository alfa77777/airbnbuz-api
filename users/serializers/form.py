from rest_framework import serializers

from users.models import AnnouncementForm


class AnnouncementFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementForm
        fields = (
            "id",
            "fullname",
            "resort_name",
            "phone",
            "address",
            "description",
            "status",
            "answer",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "answer", "created_at", "updated_at", "status")

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["user"] = user
        return super().create(validated_data)
