from django.db import models

from users.models import User


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    holder_name = models.CharField(max_length=50)
    number = models.CharField(max_length=16)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    cvc = models.CharField(max_length=10)

    def __str__(self):
        return str(self.user.full_name)
