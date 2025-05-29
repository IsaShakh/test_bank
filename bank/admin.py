from django.contrib import admin
from .models import Organization, Payment, BalanceLog

admin.site.register(Organization)
admin.site.register(Payment)
admin.site.register(BalanceLog)
