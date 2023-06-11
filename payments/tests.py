from unittest.mock import patch
# from stripe.http_client import patch

from django.http import HttpResponse
from django.http.response import HttpResponseBase
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from datetime import date

from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import data

from book.models import Book
from payments.views import CreateCheckoutSession
from payments.models import Payment, Borrowing
from user.models import Customer


class CreateCheckoutSessionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('payments.views.get_object_or_404')
    def test_create_checkout_session(self, mock_get_object_or_404):
        # Create a user
        user = Customer.objects.create(username='testuser')

        # Create a borrowing object with the expected_return_date and user_id
        expected_return_date = date.today()  # or provide a specific date
        borrowing = Borrowing.objects.create(user_id=user.id, book_id=1, expected_return_date=expected_return_date)

        url = reverse('payments:create-checkout-session')
        data = {
            'to_pay': 10,  # Provide the required data for the request
            'borrowing': borrowing.book_id,
        }
        request = self.factory.post(url, data=data)

        # Configure the mock behavior
        mock_get_object_or_404.return_value = borrowing

        # Execute the view
        view = CreateCheckoutSession.as_view()
        response = view(request)

        # Ensure the response is an appropriate instance
        self.assertIsInstance(response, (Response, HttpResponseBase), "Expected a valid response")

        # Assert the response
        if isinstance(response, HttpResponseBase):
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        else:
            self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
            self.assertIn('Location', response)

    def test_create_checkout_session_missing_data(self):
        # Create a request without the required data
        data = {}
        url = reverse('create-checkout-session')
        request = self.factory.post(url, data)

        # Execute the view
        view = CreateCheckoutSession.as_view()
        response = view(request)

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Add additional assertions as needed
