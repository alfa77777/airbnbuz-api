from django.contrib import admin

from rooms.models import Facility, Review, Room, RoomPhotos, Service


admin.site.register(Room)
admin.site.register(RoomPhotos)
admin.site.register(Review)
admin.site.register(Service)
admin.site.register(Facility)
