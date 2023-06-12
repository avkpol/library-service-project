from unittest.mock import patch

from django.http.response import HttpResponseBase
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from datetime import date

from payments.views import CreateCheckoutSession
from payments.models import Borrowing
from user.models import Customer


class CreateCheckoutSessionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch("payments.views.get_object_or_404")
    def test_create_checkout_session(self, mock_get_object_or_404):
        # Create a user
        user = Customer.objects.create(username="testuser")
        expected_return_date = date.today()
        borrowing = Borrowing.objects.create(
            user_id=user.id, book_id=1, expected_return_date=expected_return_date
        )

        url = reverse("payments:create-checkout-session")
        data = {
            "to_pay": 10,
            "borrowing": borrowing.book_id,
        }
        request = self.factory.post(url, data=data)

        mock_get_object_or_404.return_value = borrowing
        view = CreateCheckoutSession.as_view()
        response = view(request)
        self.assertIsInstance(
            response, (Response, HttpResponseBase), "Expected a valid response"
        )

        if isinstance(response, HttpResponseBase):
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        else:
            self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
            self.assertIn("Location", response)

    def test_create_checkout_session_missing_data(self):
        data = {}
        url = reverse("create-checkout-session")
        request = self.factory.post(url, data)

        view = CreateCheckoutSession.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
