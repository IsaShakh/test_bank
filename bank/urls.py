from django.urls import path
from . import views

urlpatterns = [
    path('api/webhook/bank/', views.BankWebhookView.as_view(), name='bank_webhook'),
    path('api/organizations/<str:inn>/balance/', views.OrganizationBalanceView.as_view(), name='org_balance'),
]
