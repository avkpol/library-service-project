from django.urls import include, path
from rest_framework import routers
from payments.views import CreateCheckoutSession, WebHook, PaymentListView

urlpatterns = [

    path('session/', CreateCheckoutSession.as_view(), name='create-checkout-session'),
    # path('webhook/', WebHook.as_view()),
    path('payments/successful/', PaymentListView.as_view(), name='successful-payments'),
]

app_name = "payments"
