import datetime

from rest_framework import viewsets, exceptions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingReturnSerializer
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "return_book":
            return BorrowingReturnSerializer
        return BorrowingSerializer

    def get_permissions(self):
        if self.action == "filter_by_user":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)

        if is_active is not None:
            is_active = is_active.lower() == "true"
            if is_active:
                queryset = queryset.filter(actual_return_date__isnull=True)
            else:
                queryset = queryset.exclude(actual_return_date__isnull=True)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        borrowing = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="return")
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date is not None:
            raise exceptions.ValidationError(
                "This borrowing has already been returned."
            )

        actual_return_date = request.data.get("actual_return_date")
        if not actual_return_date:
            raise exceptions.ValidationError("Please provide the actual return date.")

        borrowing.actual_return_date = datetime.datetime.now().date()
        borrowing.save()

        serializer = BorrowingReturnSerializer(borrowing)
        return Response(serializer.data, status=status.HTTP_200_OK)