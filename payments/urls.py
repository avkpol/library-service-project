from django.urls import path

from payments.views import CreateCheckoutSession, PaymentListView, PaymentDetailView

urlpatterns = [
    path('payments/session/', CreateCheckoutSession.as_view(), name='create-checkout-session'),
    path('payments/successful/', PaymentListView.as_view(), name='successful-payments'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
]

app_name = "payments"
