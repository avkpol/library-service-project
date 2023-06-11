from datetime import timedelta, datetime

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.test import APIClient

from user.models import Customer
from borrowing.models import Borrowing
from borrowing.views import BorrowingViewSet


class BorrowingViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.user = Customer.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.superuser = Customer.objects.create_superuser(username='ss@ss.ss', email='ss@ss.ss', password='superpassword')

    def test_create_borrowing(self):
        borrowing_data = {
            'user_id': self.user.id,
            'book_id': 1,
            'borrow_date': '2023-06-04',
            'return_date': '2023-06-11',
        }

        self.client.force_authenticate(user=self.superuser)
        response = self.client.post('/api/borrowings/', borrowing_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_borrowing_invalid_book_id(self):
        data = {
            'user_id': self.user.id,
            'book_id': 999
        }

        view = BorrowingViewSet.as_view({'post': 'create'})
        view.permission_classes = [IsAuthenticatedOrReadOnly]
        request = self.factory.post('/api/borrowings/', data=data)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Borrowing.objects.count(), 0)

    def test_return_book(self):
        borrowing = Borrowing.objects.create(
            user_id=self.user.id,
            book_id=1,
            expected_return_date=datetime.now() + timedelta(days=7)
        )

        view = BorrowingViewSet.as_view({'put': 'return_book'})
        view.permission_classes = [IsAuthenticated]
        request = self.factory.put(f'/api/borrowings/{borrowing.id}/return/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=borrowing.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        borrowing.refresh_from_db()
        self.assertIsNotNone(borrowing.actual_return_date)

    def test_return_book_already_returned(self):
        borrowing = Borrowing.objects.create(
            user_id=self.user.id,
            book_id=1,
            expected_return_date=datetime.now() + timedelta(days=7),
            actual_return_date='2023-06-01'
        )

        view = BorrowingViewSet.as_view({'put': 'return_book'})
        view.permission_classes = [IsAuthenticated]
        request = self.factory.put(f'/api/borrowings/{borrowing.id}/return/')
        force_authenticate(request, user=self.user)
        response = view(request, pk=borrowing.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        borrowing.refresh_from_db()
        self.assertIsNotNone(borrowing.actual_return_date)
