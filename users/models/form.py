from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from utils.regex import phone_regex


class AnnouncementForm(BaseModel):
    class AnswerStatus(models.TextChoices):
        NEW = "new", _("new")
        ANSWERED = "answered", _("answered")

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    resort_name = models.CharField(max_length=255)
    phone = models.CharField(validators=[phone_regex], max_length=15)
    address = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=32, choices=AnswerStatus.choices, default=AnswerStatus.NEW)
    answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.fullname
