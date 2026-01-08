from rest_framework import serializers
from .models import Customer, Reminder, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)
    balance = serializers.SerializerMethodField()
    statement_pdf = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "phone",
            "email",
            "created_at",
            "balance",
            "transactions",
            "statement_pdf",
        ]

    def get_balance(self, obj):
        last_txn = obj.transactions.order_by("-created_at").first()
        return last_txn.balance_after if last_txn else 0

    def get_statement_pdf(self, obj):
        if hasattr(obj, "statement_pdf") and obj.statement_pdf:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.statement_pdf.url)
        return None
