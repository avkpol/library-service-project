from django.urls import reverse

from user.models import Customer
from user.views import User

from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from borrowing.models import Borrowing
from book.models import Book


class BorrowingViewSetTestCase(APITestCase):
    def setUp(self):
        # self.user = User.objects.create_user(
        #     email="test@example.com",
        #     username="testuser",
        #     password="testpassword",
        #     first_name="John",
        #     last_name="Doe",
        # )
        # self.token = Token.objects.create(user=self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.client = APIClient()
        self.user = Customer.objects.create_user(
            email="testuser", username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)



    def test_create_borrowing(self):
        book = Book.objects.create(title="Test Book", inventory=5, daily_fee=10.0)
        borrowing_data = {
            "borrow_date": "2023-06-04",
            "expected_return_date": "2023-06-11",
            "book_id": book.id,
            "user_id": self.user.id,
        }
        # response = self.client.post(
        #     "api/borrowings/",
        #     borrowing_data,
        #     follow=True,
        # )
        response = self.client.post(reverse("borrowing:borrowing-list"), borrowing_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 1)
        borrowing = Borrowing.objects.first()
        self.assertEqual(borrowing.book_id, book.id)
        self.assertEqual(borrowing.user_id, self.user.id)

    def test_create_borrowing_invalid_book_id(self):
        borrowing_data = {
            "book_id": 999,
            "borrow_date": "2023-06-04",
            "expected_return_date": "2023-06-11",
        }
        response = self.client.post(
            "api/borrowings/",
            borrowing_data,
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Borrowing.objects.count(), 0)

    def test_return_book(self):
        book = Book.objects.create(title="Test Book", inventory=5, daily_fee=10.0)
        borrowing = Borrowing.objects.create(
            user_id=self.user.id,
            book_id=book.id,
            expected_return_date=datetime.now() + timedelta(days=7),
        )
        return_data = {"actual_return_date": "2023-06-05"}
        response = self.client.post(
            f"api/borrowings/{book.id}/return/",
            return_data,
            kwargs={"pk": borrowing.id},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        borrowing.refresh_from_db()
        self.assertIsNotNone(borrowing.actual_return_date)
        book.refresh_from_db()
        self.assertEqual(book.inventory, 6)

    def test_return_book_already_returned(self):
        book = Book.objects.create(title="Test Book", inventory=5, daily_fee=10.0)
        borrowing = Borrowing.objects.create(
            user_id=self.user.id,
            book_id=book.id,
            expected_return_date=datetime.now() + timedelta(days=7),
            actual_return_date="2023-06-01",
        )
        return_data = {"actual_return_date": "2023-06-05"}
        response = self.client.post(
            f"api/borrowings/{book.id}/return/",
            return_data,
            kwargs={"pk": borrowing.id},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        borrowing.refresh_from_db()
        self.assertEqual(borrowing.actual_return_date, "2023-06-01")
        book.refresh_from_db()
        self.assertEqual(book.inventory, 5)

    def test_filter_by_user(self):
        book = Book.objects.create(title="Test Book 1", inventory=5, daily_fee=10.0)

        borrowing_data = {
            "book_id": 999,
            "borrow_date": "2023-06-04",
            "expected_return_date": "2023-06-11",
        }

        response = self.client.get(
            f"/api/borrowings/?user_id={self.user.id}&is_active={self.user.is_active}",
            borrowing_data,
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        borrowings = response.data
        self.assertEqual(len(borrowings), 1)
        self.assertEqual(borrowings[0]["user_id"], self.user.id)
        self.assertEqual(borrowings[0]["book_id"], book.id)
