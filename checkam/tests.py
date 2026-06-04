from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Transactions, Budget
from decimal import Decimal


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@example.com', email='test@example.com',
            password='TestPass1!', first_name='Test', last_name='User'
        )

    def test_transaction_str(self):
        t = Transactions.objects.create(
            user=self.user, description='Salary', amount=50000,
            transaction_type='income', category='salary'
        )
        self.assertIn('Salary', str(t))
        self.assertIn('50000', str(t))

    def test_budget_str(self):
        b = Budget.objects.create(user=self.user, title='Groceries', limit=20000)
        self.assertEqual(str(b), 'Groceries')

    def test_transaction_creates_correctly(self):
        t = Transactions.objects.create(
            user=self.user, description='Rent', amount=30000,
            transaction_type='expense', category='rent'
        )
        self.assertEqual(t.transaction_type, 'expense')
        self.assertEqual(float(t.amount), 30000.0)

    def test_budget_limit_stored_correctly(self):
        b = Budget.objects.create(user=self.user, title='Transport', limit=15000)
        self.assertEqual(float(b.limit), 15000.0)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='dev@example.com', email='dev@example.com',
            password='DevPass1!', first_name='Dev', last_name='Bee'
        )

    def test_auth_page_loads(self):
        response = self.client.get(reverse('auth_page'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')

    def test_dashboard_accessible_when_logged_in(self):
        self.client.login(username='dev@example.com', password='DevPass1!')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_add_transaction(self):
        self.client.login(username='dev@example.com', password='DevPass1!')
        response = self.client.post(reverse('add_transaction'), {
            'description': 'Test income', 'transaction_type': 'income',
            'category': 'salary', 'amount': '10000'
        })
        self.assertRedirects(response, reverse('transactions'))
        self.assertEqual(Transactions.objects.filter(user=self.user).count(), 1)

    def test_add_budget(self):
        self.client.login(username='dev@example.com', password='DevPass1!')
        response = self.client.post(reverse('add_budget'), {
            'title': 'Food budget', 'limit': '25000'
        })
        self.assertRedirects(response, reverse('budgets'))
        self.assertEqual(Budget.objects.filter(user=self.user).count(), 1)

    def test_delete_transaction(self):
        self.client.login(username='dev@example.com', password='DevPass1!')
        t = Transactions.objects.create(
            user=self.user, description='Delete me', amount=5000,
            transaction_type='expense', category='other'
        )
        response = self.client.get(reverse('delete-transaction', args=[str(t.id)]))
        self.assertRedirects(response, reverse('transactions'))
        self.assertEqual(Transactions.objects.filter(user=self.user).count(), 0)

    def test_transactions_page_requires_login(self):
        response = self.client.get(reverse('transactions'))
        self.assertEqual(response.status_code, 302)

    def test_budgets_page_requires_login(self):
        response = self.client.get(reverse('budgets'))
        self.assertEqual(response.status_code, 302)
