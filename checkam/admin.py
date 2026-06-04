from django.contrib import admin
from .models import Budget, Transactions

# Register your models here.

admin.site.register(Transactions)
admin.site.register(Budget)
