from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from permissions import IsOwner
from users.models import AnnouncementForm
from users.serializers import AnnouncementFormSerializer


class AnnouncementFormListCreateView(generics.ListCreateAPIView):
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    serializer_class = AnnouncementFormSerializer

    def get_queryset(self):
        return AnnouncementForm.objects.filter(user=self.request.user).order_by("-created_at")


class AnnouncementFormDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsOwner,)
    queryset = AnnouncementForm.objects.all()
    serializer_class = AnnouncementFormSerializer
