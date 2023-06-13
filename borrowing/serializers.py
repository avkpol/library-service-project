from rest_framework import serializers

from borrowing.models import Borrowing
from notifications.signals import send_return_borrowing_notification
from notifications.telegram_helper import send_telegram_message


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
            "user",
        )

    def create(self, validated_data):
        book = validated_data.pop("book")
        borrowing = Borrowing.objects.create(book=book, **validated_data)
        self.update_book_inventory(book)
        self.send_telegram_message(borrowing)
        return borrowing

    def update_book_inventory(self, book):
        if book.inventory == 0:
            raise serializers.ValidationError("Book inventory is zero.")
        book.inventory -= 1
        book.save()

    def send_telegram_message(self, borrowing):
        chat_id = "YOUR_TELEGRAM_CHAT_ID"
        message = (
            f"New borrowing created!\nBorrowing ID: {borrowing.id}"
            f"\nUser ID: {borrowing.user.id}"
            f"\nBook ID: {borrowing.book.id}"
        )
        send_telegram_message(chat_id, message)


class BorrowingReturnSerializer(serializers.ModelSerializer):
    actual_return_date = serializers.DateField()

    class Meta:
        model = Borrowing
        fields = ("actual_return_date",)
        read_only_fields = (
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)

        borrowing = self.instance
        actual_return_date = attrs.get("actual_return_date")
        if not actual_return_date:
            raise serializers.ValidationError("Please provide the actual return date.")

        if borrowing.actual_return_date is not None:
            raise serializers.ValidationError("This borrowing has already been returned.")

        return attrs

    def update(self, instance, validated_data):
        actual_return_date = validated_data.get("actual_return_date")
        if not actual_return_date:
            raise serializers.ValidationError("Please provide the actual return date.")
        instance.actual_return_date = actual_return_date
        instance.save()
        self.update_book_inventory(instance.book)
        self.send_return_borrowing_notification(instance)
        return instance

    def update_book_inventory(self, book):
        book.inventory += 1
        book.save()

    def send_return_borrowing_notification(self, borrowing):
        send_return_borrowing_notification(
            sender=self.__class__, instance=borrowing
        )
