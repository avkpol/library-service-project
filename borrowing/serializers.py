from rest_framework import serializers

from book.models import Book
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
            "book_id",
            "user_id",
        )

    def create(self, validated_data):
        book_id = validated_data.pop("book_id")
        borrowing = Borrowing.objects.create(book_id=book_id, **validated_data)
        self.update_book_inventory(book_id)
        self.send_telegram_message(borrowing)
        return borrowing

    def update_book_inventory(self, book_id):
        try:
            book = Book.objects.get(id=book_id)
            if book.inventory == 0:
                raise serializers.ValidationError("Book inventory is zero.")
            book.inventory -= 1
            book.save()
        except Book.DoesNotExist:
            raise serializers.ValidationError("Invalid book ID.")

    def send_telegram_message(self, borrowing):
        chat_id = "YOUR_TELEGRAM_CHAT_ID"
        message = (
            f"New borrowing created!\nBorrowing ID: {borrowing.id}"
            f"\nUser ID: {borrowing.user_id}"
            f"\nBook ID: {borrowing.book_id}"
        )
        send_telegram_message(chat_id, message)


class BorrowingReturnSerializer(serializers.ModelSerializer):
    actual_return_date = serializers.DateField()

    class Meta:
        model = Borrowing
        fields = ("actual_return_date",)
        read_only_fields = (
            "book_id",
            "user_id",
            "borrow_date",
            "expected_return_date",
        )

    def update(self, instance, validated_data):
        actual_return_date = validated_data.get("actual_return_date")
        if not actual_return_date:
            raise serializers.ValidationError("Please provide the actual return date.")
        instance.actual_return_date = actual_return_date
        instance.save()
        book_id = instance.book_id
        self.update_book_inventory(book_id)
        self.send_return_borrowing_notification(instance)
        return instance

    def update_book_inventory(self, book_id):
        try:
            book = Book.objects.get(id=book_id)
            book.inventory += 1
            book.save()
        except Book.DoesNotExist:
            raise serializers.ValidationError("Invalid book ID.")

    def send_return_borrowing_notification(self, borrowing):
        send_return_borrowing_notification(
            sender=self.__class__, instance=borrowing
        )
