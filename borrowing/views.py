from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, exceptions, status, request
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from book.models import Book
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer
from user.models import Customer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    # authentication_classes = (JWTAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action == 'filter_by_user':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        is_active = self.request.query_params.get('is_active')

        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)

        if is_active is not None:
            is_active = is_active.lower() == 'true'
            if is_active:
                queryset = queryset.filter(actual_return_date__isnull=True)
            else:
                queryset = queryset.exclude(actual_return_date__isnull=True)

        return queryset


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_id = serializer.validated_data['book_id']
        self.validate_inventory(book_id)
        borrowing = self.perform_create(serializer, book_id)
        return Response(BorrowingSerializer(borrowing).data)

    def validate_inventory(self, book_id):
        try:
            book = Book.objects.get(id=book_id)
            if book.inventory == 0:
                raise exceptions.ValidationError("Book inventory is zero.")
        except Book.DoesNotExist:
            raise exceptions.ValidationError("Invalid book ID.")

    def perform_create(self, serializer, book_id):
        borrowing = serializer.save()
        book = get_object_or_404(Book, id=book_id)
        if book.inventory == 0:
            raise exceptions.ValidationError("The book is not available in inventory.")
        book.inventory -= 1
        book.save()
        borrowing.book = book  # Assign the book to the borrowing object
        borrowing.save()
        return borrowing
    '''
    for filtering a user by user_id and is_active use query 
    "/api/borrowings/?user_id=<user_id>&is_active=<is_active>"
    '''

    @action(detail=False, methods=['get'])
    def filter_by_user(self, request):
        user_id = request.GET.get('user_id')
        is_active = request.GET.get('is_active')

        if request.user.is_staff:
            borrowings = Borrowing.objects.all()
        else:
            borrowings = Borrowing.objects.filter(user_id=request.user.id)

        if user_id:
            if not request.user.is_staff and int(user_id) != request.user.id:
                raise exceptions.PermissionDenied("You can only access your own borrowings.")
            borrowings = borrowings.filter(user_id=user_id)

        if is_active is not None:
            if is_active.lower() == 'true':
                borrowings = borrowings.filter(actual_return_date__isnull=True)
            else:
                borrowings = borrowings.filter(actual_return_date__isnull=False)

        serializer = BorrowingSerializer(borrowings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='return')
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date is not None:
            raise exceptions.ValidationError("This borrowing has already been returned.")

        actual_return_date = request.data.get('actual_return_date')
        if not actual_return_date:
            raise exceptions.ValidationError("Please provide the actual return date.")

        borrowing.actual_return_date = actual_return_date
        borrowing.save()

        book = get_object_or_404(Book, id=borrowing.book_id)
        with transaction.atomic():
            book.inventory += 1
            book.save()

        borrowing.book = book  # Assign the book to the borrowing object
        borrowing.save()

        serializer = BorrowingSerializer(borrowing)
        return Response(serializer.data, status=status.HTTP_200_OK)




