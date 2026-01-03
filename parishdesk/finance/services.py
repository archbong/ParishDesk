from .models import AccountTransaction

def create_transaction(church, contributor, amount, transaction_type, notes=""):
    return AccountTransaction.objects.create(
        church=church,
        contributor=contributor,
        amount=amount,
        transaction_type=transaction_type,
        notes=notes,
    )

def update_transaction(transaction, **data):
    for key, value in data.items():
        setattr(transaction, key, value)
    transaction.save()
    return transaction

def get_church_total(church, transaction_type=None):
    qs = AccountTransaction.objects.filter(church=church)
    if transaction_type:
        qs = qs.filter(transaction_type=transaction_type)
    return qs.aggregate(total=models.Sum("amount"))["total"] or 0
