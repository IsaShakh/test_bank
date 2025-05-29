from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Organization, Payment, BalanceLog
from django.db import models
import logging

logger = logging.getLogger(__name__)

class BankWebhookView(APIView):
    def post(self, request):
        data = request.data
        operation_id = data.get("operation_id")

        if Payment.objects.filter(operation_id=operation_id).exists():
            return Response({"status": "дубликат"}, status=status.HTTP_200_OK)

        try:
            with transaction.atomic():
                payment = Payment.objects.create(
                    operation_id=operation_id,
                    amount=data["amount"],
                    payer_inn=data["payer_inn"],
                    document_number=data["document_number"],
                    document_date=data["document_date"],
                )

                org, _ = Organization.objects.get_or_create(inn=payment.payer_inn)
                org.balance = models.F("balance") + payment.amount
                org.save()

                BalanceLog.objects.create(
                    organization=org,
                    amount=payment.amount,
                    comment=f"вебхук: {payment.document_number}"
                )

                logger.info(f"Баланс по инн {org.inn} увеличен на {payment.amount}")
                return Response({"status": "created"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"error : {e}")
            return Response({"error": "internal_error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrganizationBalanceView(APIView):
    def get(self, request, inn):
        try:
            org = Organization.objects.get(inn=inn)
            return Response({
                "inn": org.inn,
                "balance": org.balance
            }, status=status.HTTP_200_OK)
        except Organization.DoesNotExist:
            return Response({"error": "орагнизация не существует"}, status=status.HTTP_404_NOT_FOUND)
