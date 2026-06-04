import re, csv
from datetime import date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, resolve_url
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Transactions, Budget, Signup


# ──────────────────────────── AUTH ────────────────────────────

def auth_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'signup':
            username = request.POST.get('username', '').strip().lower()
            first_name = request.POST.get('first_name', '').strip().capitalize()
            last_name  = request.POST.get('last_name',  '').strip().capitalize()
            email      = request.POST.get('email', '').strip().lower()
            password   = request.POST.get('password', '')

            if not all([username, first_name, last_name, email, password]):
                messages.error(request, 'Please fill all the fields')
                return render(request, 'auth/auth_page.html')
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return render(request, 'auth/auth_page.html')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return render(request, 'auth/auth_page.html')
            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters.')
                return render(request, 'auth/auth_page.html')
            if not re.search(r'[A-Z]', password):
                messages.error(request, 'Password must contain an uppercase letter.')
                return render(request, 'auth/auth_page.html')
            if not re.search(r'[a-z]', password):
                messages.error(request, 'Password must contain a lowercase letter.')
                return render(request, 'auth/auth_page.html')
            if not re.search(r'\d', password):
                messages.error(request, 'Password must contain a number.')
                return render(request, 'auth/auth_page.html')
            if not re.search(r'[@$!%*?&]', password):
                messages.error(request, 'Password must contain a special character (@$!%*?&).')
                return render(request, 'auth/auth_page.html')

            signup = Signup.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            user = User.objects.create_user(username=signup.username, first_name=signup.first_name, last_name=signup.last_name, email=signup.email)
            user.set_password(signup.password)
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')

        elif form_type == 'signin':
            email    = request.POST.get('email', '').strip().lower()
            password = request.POST.get('password', '')
            if not email or not password:
                messages.error(request, 'Please fill all the fields')
                return render(request, 'auth/auth_page.html')
            if not User.objects.filter(email=email).exists():
                messages.error(request, 'User not found')
                return render(request, 'auth/auth_page.html')
            user = authenticate(request, username=email, password=password)
            if not user:
                messages.error(request, 'Incorrect password')
                return render(request, 'auth/auth_page.html')
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('dashboard')

    return render(request, 'auth/auth_page.html')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('auth_page')


# ──────────────────────────── DASHBOARD ────────────────────────────

@login_required
def dashboard(request):
    txns    = Transactions.objects.filter(user=request.user).order_by('-date')
    income  = txns.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
    expense = txns.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0
    balance = income - expense
    savings_rate = round((balance / income * 100), 2) if income > 0 else 0
    return render(request, 'dashboard/dashboard.html', {
        'transactions': txns[:5],
        'income': income, 'expense': expense,
        'balance': balance, 'savings_rate': savings_rate,
    })


# ──────────────────────────── TRANSACTIONS ────────────────────────────

@login_required
def transactions(request):
    txns    = Transactions.objects.filter(user=request.user).order_by('-date')
    income  = txns.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
    expense = txns.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0
    balance = income - expense
    savings_rate = round((balance / income * 100), 2) if income > 0 else 0
    return render(request, 'transactions/transactions.html', {
        'transactions': txns,
        'income': income, 'expense': expense,
        'balance': balance, 'savings_rate': savings_rate,
    })


class GetTransactionsAPI(LoginRequiredMixin, View):
    def get(self, request):
        txns = Transactions.objects.filter(user=request.user).order_by('-date')
        data = [{'id': str(t.id), 'description': t.description, 'category': t.category,
                 'transaction_type': t.transaction_type, 'amount': float(t.amount),
                 'date': t.date.strftime('%Y-%m-%d')} for t in txns]
        return JsonResponse({'success': True, 'transactions': data})


class AddTransaction(LoginRequiredMixin, View):
    def post(self, request):
        description      = request.POST.get('description', '').strip()
        transaction_type = request.POST.get('transaction_type', '')
        category         = request.POST.get('category', '')
        amount           = request.POST.get('amount', '')

        if not all([description, transaction_type, category, amount]):
            messages.error(request, 'All fields are required')
            return redirect('transactions')
        try:
            amt = float(amount)
            if amt <= 0: raise ValueError
        except ValueError:
            messages.error(request, 'Amount must be a positive number')
            return redirect('transactions')

        Transactions.objects.create(user=request.user, description=description,
                                    transaction_type=transaction_type, category=category, amount=amt)
        messages.success(request, 'Transaction added')
        return redirect('transactions')


class EditTransaction(LoginRequiredMixin, View):
    def post(self, request, transaction_id):
        txn = Transactions.objects.filter(id=transaction_id, user=request.user).first()
        if not txn:
            messages.error(request, 'Transaction not found')
            return redirect('transactions')

        description      = request.POST.get('description', '').strip()
        transaction_type = request.POST.get('transaction_type', '')
        category         = request.POST.get('category', '')
        amount           = request.POST.get('amount', '')

        if not all([description, transaction_type, category, amount]):
            messages.error(request, 'All fields are required')
            return redirect('transactions')
        try:
            amt = float(amount)
            if amt <= 0: raise ValueError
        except ValueError:
            messages.error(request, 'Amount must be a positive number')
            return redirect('transactions')

        txn.description      = description
        txn.transaction_type = transaction_type
        txn.category         = category
        txn.amount           = amt
        txn.save()
        messages.success(request, 'Transaction updated')
        return redirect('transactions')


class DeleteTransaction(LoginRequiredMixin, View):
    def get(self, request, transaction_id):
        txn = Transactions.objects.filter(id=transaction_id, user=request.user).first()
        if txn:
            txn.delete()
            messages.success(request, 'Transaction deleted')
        else:
            messages.error(request, 'Transaction not found')
        return redirect('transactions')


# ──────────────────────────── BUDGETS ────────────────────────────

CATEGORY_LABELS = dict([
    ('food', 'Food'), ('transport', 'Transport'), ('rent', 'Rent'),
    ('data', 'Data'), ('salary', 'Salary'), ('entertainment', 'Entertainment'),
    ('utilities', 'Utilities'), ('other', 'Other'),
])

class BudgetsView(LoginRequiredMixin, View):
    def get(self, request):
        budgets = Budget.objects.filter(user=request.user)
        # Which categories already have a budget (to hide them from Add modal)
        used_categories = set(budgets.values_list('category', flat=True))
        available_categories = [(k, v) for k, v in CATEGORY_LABELS.items() if k not in used_categories]

        for b in budgets:
            # Spent = sum of expense transactions in THIS specific category
            spent = (Transactions.objects
                     .filter(user=request.user, transaction_type='expense', category=b.category)
                     .aggregate(total=Sum('amount'))['total'] or 0)
            b.spent        = float(spent)
            b.remaining    = max(float(b.limit) - float(spent), 0)
            b.overspent    = max(float(spent) - float(b.limit), 0)
            b.percent      = min(round((float(spent) / float(b.limit)) * 100), 100) if b.limit else 0
            b.over_budget  = float(spent) > float(b.limit)
            b.category_label = CATEGORY_LABELS.get(b.category, b.category.capitalize())

        return render(request, 'budgets/budgets.html', {
            'budgets': budgets,
            'available_categories': available_categories,
        })


class AddBudgetView(LoginRequiredMixin, View):
    def post(self, request):
        category = request.POST.get('category', '').strip()
        limit    = request.POST.get('limit', '')
        if not category or not limit:
            messages.error(request, 'All fields are required')
            return redirect('budgets')
        try:
            limit_amt = float(limit)
            if limit_amt <= 0: raise ValueError
        except ValueError:
            messages.error(request, 'Limit must be a positive number')
            return redirect('budgets')
        if Budget.objects.filter(user=request.user, category=category).exists():
            messages.error(request, 'A budget for that category already exists')
            return redirect('budgets')
        Budget.objects.create(user=request.user, category=category, limit=limit_amt)
        messages.success(request, 'Budget added successfully')
        return redirect('budgets')


@login_required
def edit_budget(request, budget_id):
    budget = Budget.objects.filter(id=budget_id, user=request.user).first()
    if not budget:
        messages.error(request, 'Budget not found')
        return redirect('budgets')
    if request.method == 'POST':
        category = request.POST.get('category', '').strip()
        limit    = request.POST.get('limit', '')
        if not category or not limit:
            messages.error(request, 'All fields are required')
            return redirect('budgets')
        try:
            limit_amt = float(limit)
            if limit_amt <= 0: raise ValueError
        except ValueError:
            messages.error(request, 'Limit must be a positive number')
            return redirect('budgets')
        budget.category = category
        budget.limit    = limit_amt
        budget.save()
        messages.success(request, 'Budget updated successfully')
    return redirect('budgets')


class DeleteBudgetView(LoginRequiredMixin, View):
    def get(self, request, budget_id):
        budget = Budget.objects.filter(id=budget_id, user=request.user).first()
        if budget:
            budget.delete()
            messages.success(request, 'Budget deleted')
        else:
            messages.error(request, 'Budget not found')
        return redirect('budgets')


# ──────────────────────────── REPORTS & APIs ────────────────────────────

@login_required
def reports(request):
    return render(request, 'reports/reports.html')


class MonthlySummaryAPI(LoginRequiredMixin, View):
    def get(self, request):
        six_months_ago = (date.today().replace(day=1) - timedelta(days=150))
        rows = (Transactions.objects
                .filter(user=request.user, date__gte=six_months_ago)
                .annotate(month=TruncMonth('date'))
                .values('month', 'transaction_type')
                .annotate(total=Sum('amount'))
                .order_by('month'))
        summary = {}
        for row in rows:
            key = row['month'].strftime('%b %Y')
            summary.setdefault(key, {'income': 0, 'expense': 0})
            summary[key][row['transaction_type']] = float(row['total'])
        return JsonResponse({'success': True, 'summary': summary})


class CategorySummaryAPI(LoginRequiredMixin, View):
    def get(self, request):
        rows = (Transactions.objects
                .filter(user=request.user, transaction_type='expense')
                .values('category')
                .annotate(total=Sum('amount'))
                .order_by('-total')[:10])
        data = [{'label': r['category'].capitalize(), 'value': float(r['total'])} for r in rows]
        return JsonResponse({'success': True, 'categories': data})


class BudgetPerformanceAPI(LoginRequiredMixin, View):
    def get(self, request):
        budgets = Budget.objects.filter(user=request.user)
        data = []
        for b in budgets:
            spent = (Transactions.objects
                     .filter(user=request.user, transaction_type='expense')
                     .aggregate(total=Sum('amount'))['total'] or 0)
            data.append({'title': b.title, 'limit': float(b.limit), 'spent': float(spent)})
        return JsonResponse({'success': True, 'budgets': data})


@login_required
def export_csv(request):
    txns = Transactions.objects.filter(user=request.user).order_by('-date')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="checkam_transactions.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Description', 'Type', 'Category', 'Amount (₦)'])
    for t in txns:
        writer.writerow([t.date.strftime('%Y-%m-%d'), t.description,
                         t.transaction_type, t.category, f'{t.amount:.2f}'])
    return response


# ──────────────────────────── SETTINGS ────────────────────────────

@login_required
def settings_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            first_name = request.POST.get('first_name', '').strip().capitalize()
            last_name  = request.POST.get('last_name',  '').strip().capitalize()
            if first_name: request.user.first_name = first_name
            if last_name:  request.user.last_name  = last_name
            request.user.save()
            messages.success(request, 'Profile updated successfully')

        elif action == 'change_password':
            current = request.POST.get('current_password', '')
            new_pw  = request.POST.get('new_password', '')
            confirm = request.POST.get('confirm_password', '')
            if not request.user.check_password(current):
                messages.error(request, 'Current password is incorrect')
            elif new_pw != confirm:
                messages.error(request, 'New passwords do not match')
            elif len(new_pw) < 8:
                messages.error(request, 'Password must be at least 8 characters')
            else:
                request.user.set_password(new_pw)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully')

        return redirect('settings')

    return render(request, 'settings/settings.html')


# ──────────────────────────── MISC ────────────────────────────

class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'auth/forgot_password.html')
    def post(self, request):
        pass
