from django.db import models
from django.contrib.auth.models import User
import uuid

CATEGORY_CHOICES = [
    ('food', 'Food'),
    ('transport', 'Transport'),
    ('rent', 'Rent'),
    ('data', 'Data'),
    ('salary', 'Salary'),
    ('entertainment', 'Entertainment'),
    ('utilities', 'Utilities'),
    ('other', 'Other'),
]

class Signup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class Transactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('income', 'Income'), ('expense', 'Expense')])
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.description} - {self.amount}"

class Budget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    limit = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return self.get_category_display()
