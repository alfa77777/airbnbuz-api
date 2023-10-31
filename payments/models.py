import stripe
from django.conf import settings
from django.db import models

from card.models import Card


class Payment(models.Model):
    class PaymentStatuses(models.TextChoices):
        SUCCESS = "success"
        FAILED = "failed"

    amount = models.FloatField()
    currency = models.CharField(max_length=16)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="payments")
    status = models.CharField(max_length=32, choices=PaymentStatuses.choices)

    @staticmethod
    def token(card_number, exp_month, exp_year, cvc):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        return stripe.Token.create(
            card={"number": card_number, "exp_month": exp_month, "exp_year": exp_year, "cvc": cvc}
        )

    def process_payment(self, source):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Create a Stripe charge
        charge = stripe.Charge.create(amount=self.amount, currency=self.currency, source=source)

        # Handle the charge response as needed
        if charge.paid:
            self.status = "success"
        else:
            self.status = "failed"
        self.save()
