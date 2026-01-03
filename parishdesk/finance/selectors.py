from .models import AccountTransaction

def list_transactions_for_church(church, transaction_type=None):
    qs = AccountTransaction.objects.filter(church=church)
    if transaction_type:
        qs = qs.filter(transaction_type=transaction_type)
    return qs.order_by("-created_at")

def get_transaction_detail(transaction_id):
    return AccountTransaction.objects.get(pk=transaction_id)
