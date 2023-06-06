from rest_framework.response import Response
from rest_framework import permissions, viewsets

from book.models import Book
from book.serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes_by_action = {
    #     'list': [permissions.AllowAny],
    #     'create': [permissions.IsAdminUser],
    #     'retrieve': [permissions.IsAdminUser],
    #     'update': [permissions.IsAdminUser],
    #     'partial_update': [permissions.IsAdminUser],
    #     'destroy': [permissions.IsAdminUser],
    # }

    # def get_permissions(self):
    #     try:
    #         return [permission() for permission in self.permission_classes_by_action[self.action]]
    #     except KeyError:
    #         return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

