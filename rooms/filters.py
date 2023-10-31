import django_filters

from rooms.models import Room


class RoomFilter(django_filters.FilterSet):
    region_name = django_filters.CharFilter(field_name="region__name", lookup_expr="icontains")
    facility_name = django_filters.CharFilter(field_name="facilities__name", lookup_expr="icontains")

    class Meta:
        model = Room
        fields = ["region_name", "guests", "facility_name"]
