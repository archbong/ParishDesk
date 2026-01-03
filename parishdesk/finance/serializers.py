from rest_framework import serializers
from .models import AccountTransaction

class AccountTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountTransaction
        fields = "__all__"
        read_only_fields = ["created_at", "contributor"]

