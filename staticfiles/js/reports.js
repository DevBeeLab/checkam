// ── reports.js ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  if (typeof Chart === 'undefined') return;

  // ── Monthly Income vs Expense bar chart ────────────────
  fetch('/api/monthly-summary/')
    .then(r => r.json())
    .then(({ summary }) => {
      const labels   = Object.keys(summary);
      const incomes  = labels.map(k => summary[k].income  || 0);
      const expenses = labels.map(k => summary[k].expense || 0);

      const ctx = document.getElementById('monthlySpendingChart');
      if (ctx) {
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels,
            datasets: [
              { label: 'Income',  data: incomes,  backgroundColor: '#1E8449' },
              { label: 'Expense', data: expenses, backgroundColor: '#C0392B' }
            ]
          },
          options: {
            responsive: true,
            plugins: { legend: { position: 'bottom' } },
            scales: { y: { beginAtZero: true } }
          }
        });
      }
    });

  // ── Category breakdown doughnut ─────────────────────────
  fetch('/api/category-summary/')
    .then(r => r.json())
    .then(({ categories }) => {
      if (!categories?.length) return;
      const ctx = document.getElementById('categoryBreakdownChart');
      if (ctx) {
        new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: categories.map(c => c.label),
            datasets: [{
              data: categories.map(c => c.value),
              backgroundColor: ['#0A3D62','#1E8449','#C0392B','#F39C12','#8E44AD','#16A085','#2980B9','#D35400'],
              borderWidth: 0
            }]
          },
          options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
        });
      }
    });

  // ── Budget Performance bar chart ────────────────────────
  fetch('/api/budget-performance/')
    .then(r => r.json())
    .then(({ budgets }) => {
      if (!budgets?.length) return;
      const ctx = document.getElementById('budgetPerformanceChart');
      if (ctx) {
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: budgets.map(b => b.title),
            datasets: [
              { label: 'Limit', data: budgets.map(b => b.limit), backgroundColor: '#0A3D62' },
              { label: 'Spent', data: budgets.map(b => b.spent), backgroundColor: '#C0392B' }
            ]
          },
          options: {
            responsive: true,
            plugins: { legend: { position: 'bottom' } },
            scales: { y: { beginAtZero: true } }
          }
        });
      }
    });

  // ── CSV Export ──────────────────────────────────────────
  document.getElementById('exportCsvBtn')?.addEventListener('click', () => {
    window.location.href = '/export-csv/';
  });
});
