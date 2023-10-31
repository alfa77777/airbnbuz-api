from django.contrib import admin

from card.models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    fields = ["id", "user", "name", "number"]
