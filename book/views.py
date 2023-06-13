from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)
from book.models import Book
from book.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()
