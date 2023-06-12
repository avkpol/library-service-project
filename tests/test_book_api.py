from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from user.models import Customer
from book.models import Book


class BookViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Customer.objects.create_user(
            email="testuser", username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_list_books(self):

        Book.objects.create(
            title="Book 1", author="Author 1", cover="H", inventory=10, daily_fee="9.99"
        )
        Book.objects.create(
            title="Book 2", author="Author 2", cover="S", inventory=5, daily_fee="4.99"
        )

        response = self.client.get(reverse("book:book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    def test_retrieve_book(self):
        book = Book.objects.create(
            title="Book 1", author="Author 1", cover="H", inventory=10, daily_fee="9.99"
        )

        response = self.client.get(reverse("book:book-detail", kwargs={"pk": book.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["title"], "Book 1"
        )

    def test_create_book(self):
        book_data = {
            "title": "New Book",
            "author": "Author",
            "cover": "H",
            "inventory": 10,
            "daily_fee": "9.99",
        }

        response = self.client.post(reverse("book:book-list"), book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)

    def test_update_book(self):
        book = Book.objects.create(
            title="Book 1", author="Author 1", cover="H", inventory=10, daily_fee="9.99"
        )
        updated_data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "cover": "S",
            "inventory": 5,
            "daily_fee": "4.99",
        }

        response = self.client.put(
            reverse("book:book-detail", kwargs={"pk": book.pk}), updated_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, "Updated Book")

    def test_delete_book(self):
        book = Book.objects.create(
            title="Book 1", author="Author 1", cover="H", inventory=10, daily_fee="9.99"
        )

        response = self.client.delete(
            reverse("book:book-detail", kwargs={"pk": book.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
