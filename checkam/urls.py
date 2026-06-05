from django.urls import path
from checkam.views import *

# Custom error handlers — Django picks these up automatically
handler404 = 'checkam.views.handler404'
handler500 = 'checkam.views.handler500'

urlpatterns = [
    path('', landing, name='landing'),
    path('auth/', auth_page, name='auth_page'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('dashboard/', dashboard, name='dashboard'),
    path('transactions/', transactions, name='transactions'),
    path('api/transactions/', GetTransactionsAPI.as_view(), name='api_transactions'),
    path('api/monthly-summary/', MonthlySummaryAPI.as_view(), name='api_monthly_summary'),
    path('api/category-summary/', CategorySummaryAPI.as_view(), name='api_category_summary'),
    path('api/budget-performance/', BudgetPerformanceAPI.as_view(), name='api_budget_performance'),
    path('add-transaction/', AddTransaction.as_view(), name='add_transaction'),
    path('edit-transaction/<str:transaction_id>', EditTransaction.as_view(), name='edit-transaction'),
    path('delete-transaction/<str:transaction_id>', DeleteTransaction.as_view(), name='delete-transaction'),
    path('budgets/', BudgetsView.as_view(), name='budgets'),
    path('add-budget/', AddBudgetView.as_view(), name='add_budget'),
    path('edit-budget/<str:budget_id>', edit_budget, name='edit_budget'),
    path('delete-budget/<str:budget_id>', DeleteBudgetView.as_view(), name='delete_budget'),
    path('reports/', reports, name='reports'),
    path('export-csv/', export_csv, name='export_csv'),
    path('settings/', settings_view, name='settings'),
    path('logout/', LogoutView.as_view(), name='logout'),
]