from rest_framework import serializers

from card.models import Card


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ("id", "holder_name", "number", "exp_month", "exp_year", "cvc")

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user

        return super().create(validated_data)
