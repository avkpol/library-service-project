from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from book.models import Book
from borrowing.models import Borrowing


class BorrowingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            title='Book Title',
            author='Book Author',
            cover='H',
            inventory=5,
            daily_fee=1.99
        )
        self.user_id = 1

    def test_create_borrowing(self):
        url = reverse('borrowing-list')
        data = {
            'borrow_date': '2022-01-01',
            'expected_return_date': '2022-01-15',
            'book_id': self.book.id,
            'user_id': self.user_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        borrowing = Borrowing.objects.get(pk=response.data['id'])
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.user_id, self.user_id)
        self.assertEqual(borrowing.actual_return_date, None)

    def test_return_book(self):
        borrowing = Borrowing.objects.create(
            borrow_date='2022-01-01',
            expected_return_date='2022-01-15',
            book_id=self.book.id,
            user_id=self.user_id
        )
        url = reverse('borrowing-return', kwargs={'pk': borrowing.pk})
        data = {'actual_return_date': '2022-01-16'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        borrowing.refresh_from_db()
        self.assertEqual(borrowing.actual_return_date, '2022-01-16')
        self.assertEqual(self.book.inventory, 6)

    def test_filter_by_user(self):
        Borrowing.objects.create(
            borrow_date='2022-01-01',
            expected_return_date='2022-01-15',
            book_id=self.book.id,
            user_id=self.user_id
        )
        Borrowing.objects.create(
            borrow_date='2022-01-02',
            expected_return_date='2022-01-16',
            book_id=self.book.id,
            user_id=self.user_id
        )
        Borrowing.objects.create(
            borrow_date='2022-01-03',
            expected_return_date='2022-01-17',
            book_id=self.book.id,
            user_id=self.user_id + 1  # Different user ID
        )
        url = reverse('borrowing-filter-by-user')
        data = {'user_id': self.user_id}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_user_non_staff(self):
        Borrowing.objects.create(
            borrow_date='2022-01-01',
            expected_return_date='2022-01-15',
            book_id=self.book.id,
            user_id=self.user_id
        )
        Borrowing.objects.create(
            borrow_date='2022-01-02',
            expected_return_date='2022-01-16',
            book_id=self.book.id,
            user_id=self.user_id
        )
        url = reverse('borrowing-filter-by-user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BorrowingAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            title='Book Title',
            author='Book Author',
            cover='H',
            inventory=5,
            daily_fee=1.99
        )
        self.user_id = 1

    def test_list_borrowings(self):
        Borrowing.objects.create(
            borrow_date='2022-01-01',
            expected_return_date='2022-01-15',
            book_id=self.book.id,
            user_id=self.user_id
        )
        Borrowing.objects.create(
            borrow_date='2022-01-02',
            expected_return_date='2022-01-16',
            book_id=self.book.id,
            user_id=self.user_id
        )
        url = reverse('borrowing-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_borrowing(self):
        borrowing = Borrowing.objects.create(
            borrow_date='2022-01-01',
            expected_return_date='2022-01-15',
            book_id=self.book.id,
            user_id=self.user_id
        )
        url = reverse('borrowing-detail', kwargs={'pk': borrowing.pk})
        data = {
            'borrow_date': '2022-01-02',
            'expected_return_date': '2022-01-16',
            'book_id': self.book.id,
            'user_id': self.user_id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        borrowing.refresh_from_db()
        self.assertEqual(borrowing.borrow_date.strftime('%Y-%m-%d'), '2022-01-02')
        self.assertEqual(borrowing.expected_return_date.strftime('%Y-%m-%d'), '2022-01-16')

    def test_delete_borrowing(self):
        borrowing = Borrowing.objects.create(
            borrow_date='2022-01-01',
            expected_return_date='2022-01-15',
            book_id=self.book.id,
            user_id=self.user_id
        )
        url = reverse('borrowing-detail', kwargs={'pk': borrowing.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Borrowing.objects.filter(pk=borrowing.pk).exists())
