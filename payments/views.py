import stripe
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from borrowing.models import Borrowing
from library_service_project import settings
from payments.models import Payment
from payments.serializers import PaymentSerializer
from rest_framework import viewsets, status

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET

REST_API_CHECKOUT_SUCCESS_URL = settings.CHECKOUT_SUCCESS_URL
REST_API_CHECKOUT_CANCEL_URL = settings.CHECKOUT_CANCEL_URL



class CreateCheckoutSession(APIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request):
        dataDict = dict(request.data)
        price = dataDict['to_pay'][0]
        borrowing_id = dataDict['borrowing'][0]
        try:
            borrowing = get_object_or_404(Borrowing, pk=borrowing_id)
            payment = Payment(borrowing=borrowing)
            unit_amount = int(payment.money_to_pay*100)
            print(unit_amount)
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': str(borrowing.book_id),
                        },
                        'unit_amount': unit_amount
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=REST_API_CHECKOUT_SUCCESS_URL,
                cancel_url=REST_API_CHECKOUT_CANCEL_URL,
            )
            payment.save()
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            print(e)
            return e
            # return JsonResponse({'error': str(e)}, status=500)


class PaymentListView(APIView):
    def get(self, request):
        payments = Payment.objects.filter(status=True)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)



class WebHook(APIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self , request):
        event = None
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
              payload, sig_header, webhook_secret
              )
        except ValueError as err:
            # Invalid payload
            raise err
        except stripe.error.SignatureVerificationError as err:
            # Invalid signature
            raise err

        # Handle the event
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
            print("--------payment_intent ---------->" , payment_intent)
        elif event.type == 'payment_method.attached':
            payment_method = event.data.object
            print("--------payment_method ---------->" , payment_method)
          # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event.type))

        return JsonResponse(success=True, safe=False)
