from django.db import models
from django.contrib.auth.models import User
from core.models import Church

class AccountTransaction(models.Model):
    TRANSACTION_TYPES = [
        ("TITHE", "Tithe"),
        ("OFFERING", "Offering"),
        ("WELFARE", "Welfare"),
        ("BUILDING", "Building Support"),
    ]

    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name="transactions")
    contributor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} ({self.church.name})"
