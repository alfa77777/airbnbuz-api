from datetime import datetime

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from bookings.models import Booking
from bookings.serializers import BookingListSerializer, BookingForPaymentSerializer
from rooms.models import Room

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET

FRONTEND_CHECKOUT_SUCCESS_URL = settings.CHECKOUT_SUCCESS_URL
FRONTEND_CHECKOUT_FAILED_URL = settings.CHECKOUT_FAILED_URL


class CreateCheckoutSession(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=BookingForPaymentSerializer)
    def post(self, request):
        data_dict = dict(request.data)
        print(data_dict)
        price = data_dict["price"]
        room = data_dict["room_slug"]
        date_in_str = data_dict["date_in"]
        date_out_str = data_dict["date_out"]
        guests = data_dict["guests"]

        date_format = "%Y-%m-%d"
        date_in = datetime.strptime(date_in_str, date_format).date()
        date_out = datetime.strptime(date_out_str, date_format).date()
        duration = (date_out - date_in).days
        total_price = price * duration
        room = Room.objects.get(slug=room)
        booking, _ = Booking.objects.get_or_create(date_in=date_in, date_out=date_out, room=room, guests=guests,
                                                   user=request.user)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": room,
                            },
                            "unit_amount": total_price,
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=f"{settings.SITE_URL}/rooms/{room}/",
                cancel_url=FRONTEND_CHECKOUT_FAILED_URL,
            )
            booking.status = booking.ApplyStatus.PAID
            booking.save()
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            print(e)
            return e


class WebHook(APIView):
    def post(self, request):
        event = None
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except ValueError as err:
            # Invalid payload
            raise err
        except stripe.error.SignatureVerificationError as err:  # noqa
            # Invalid signature
            raise err

        # Handle the event
        if event.type == "payment_intent.succeeded":
            payment_intent = event.data.object
            print("--------payment_intent ---------->", payment_intent)
        elif event.type == "payment_method.attached":
            payment_method = event.data.object
            print("--------payment_method ---------->", payment_method)
        # ... handle other event types
        else:
            print("Unhandled event type {}".format(event.type))

        return JsonResponse(success=True, safe=False)
