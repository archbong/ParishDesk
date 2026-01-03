from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import AccountTransaction
from .serializers import AccountTransactionSerializer
from .services import create_transaction, update_transaction, get_church_total
from .selectors import list_transactions_for_church, get_transaction_detail
from .permissions import IsChurchAdminOrTreasurer

class AccountTransactionViewSet(viewsets.ModelViewSet):
    queryset = AccountTransaction.objects.all()
    serializer_class = AccountTransactionSerializer
    permission_classes = [IsAuthenticated, IsChurchAdminOrTreasurer]

    def get_queryset(self):
        church_id = self.request.query_params.get("church")
        transaction_type = self.request.query_params.get("transaction_type")
        if not church_id:
            return AccountTransaction.objects.none()
        from core.models import Church
        church = Church.objects.get(pk=church_id)
        return list_transactions_for_church(church=church, transaction_type=transaction_type)

    def perform_create(self, serializer):
        church_id = self.request.data.get("church")
        from core.models import Church
        church = Church.objects.get(pk=church_id)
        serializer.instance = create_transaction(
            church=church,
            contributor=self.request.user,
            amount=serializer.validated_data.get("amount"),
            transaction_type=serializer.validated_data.get("transaction_type"),
            notes=serializer.validated_data.get("notes", "")
        )

    def perform_update(self, serializer):
        transaction = serializer.instance
        serializer.instance = update_transaction(transaction, **serializer.validated_data)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def total(self, request):
        church_id = request.query_params.get("church")
        transaction_type = request.query_params.get("transaction_type")
        from core.models import Church
        church = Church.objects.get(pk=church_id)
        total_amount = get_church_total(church, transaction_type)
        return Response({"total": total_amount})
