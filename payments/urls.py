from django.urls import path

from payments.views import (
    CreateCheckoutSession,
    PaymentListView,
    PaymentDetailView,
    CustomSuccessView,
    WebHook
)

urlpatterns = [
    path(
        "payments/session/",
        CreateCheckoutSession.as_view(),
        name="create-checkout-session",
    ),
    path(
        "payments/", PaymentListView.as_view(),
        name="successful-payments"
    ),
    path(
        "payments/<int:pk>/", PaymentDetailView.as_view(),
        name="payment-detail"
    ),
    path(
        "payments/success/", CustomSuccessView.as_view(),
        name="payments-successful"
    ),
    path("webhook/", WebHook.as_view(), name="webhook"),


]

app_name = "payments"
