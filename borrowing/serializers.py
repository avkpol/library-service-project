from rest_framework import serializers
from .models import Borrowing

class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowingReturnSerializer(serializers.Serializer):
    # actual_return_date = serializers.DateField()

    class Meta:
        model = Borrowing
        fields = ('actual_return_date',)
        read_only_fields = (
            "expected_return_date",
            "borrow_date",

        )

