from rest_framework import serializers
from borrowing.models import Borrowing

class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date", "book_id", "user_id",)

    def create(self, validated_data):
        book_id = validated_data.pop('book_id')
        borrowing = Borrowing.objects.create(book_id=book_id, **validated_data)
        return borrowing

class BorrowingReturnSerializer(serializers.ModelSerializer):
    actual_return_date = serializers.DateField()

    class Meta:
        model = Borrowing
        fields = ('actual_return_date', )
        read_only_fields = ('book_id', 'user_id', "borrow_date", "expected_return_date",)


