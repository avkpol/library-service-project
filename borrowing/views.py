from rest_framework import viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response

from book.models import Book
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validate_inventory(serializer.validated_data['book_id'])
        borrowing = self.perform_create(serializer)
        return Response(BorrowingSerializer(borrowing).data)

    def validate_inventory(self, book_id):
        try:
            book = Book.objects.get(id=book_id)
            if book.inventory == 0:
                raise exceptions.ValidationError("Book inventory is zero.")
        except Book.DoesNotExist:
            raise exceptions.ValidationError("Invalid book ID.")


    def perform_create(self, serializer):
        borrowing = serializer.save()
        # Decrease inventory count by 1 when a book is borrowed
        book_id = borrowing.book_id
        # Your code to decrease inventory count for the book goes here
        return borrowing

    @action(detail=False, methods=['get'])
    def filter_by_user(self, request):
        user_id = request.GET.get('user_id')
        is_active = request.GET.get('is_active')
        borrowings = Borrowing.objects.filter(user_id=user_id)
        if is_active is not None:
            borrowings = borrowings.filter(actual_return_date__isnull=is_active.lower() == 'true')
        serializer = BorrowingSerializer(borrowings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        borrowing.actual_return_date = request.data.get('actual_return_date')
        borrowing.save()
        # Increase inventory count by 1 when a book is returned
        book_id = borrowing.book_id
        # Your code to increase inventory count for the book goes here
        serializer = BorrowingSerializer(borrowing)
        return Response(serializer.data)
