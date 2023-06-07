from django.urls import include, path
from rest_framework import routers
from payments.views import CreateCheckoutSession, WebHook

urlpatterns = [

    path('session/', CreateCheckoutSession.as_view()),
    path('webhook/', WebHook.as_view()),
]

app_name = "payments"
