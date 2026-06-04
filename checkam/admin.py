from django.contrib import admin
from .models import Budget, Signup, Transactions

# Register your models here.

admin.site.register(Signup)
admin.site.register(Transactions)
admin.site.register(Budget)
