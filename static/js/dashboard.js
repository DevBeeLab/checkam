// ── dashboard.js ────────────────────────────────────────────
// Chart.js is loaded BEFORE this script in the template (extra_js block),
// so Chart is always available here.

function initDashboardCharts() {
  const income  = Number(document.getElementById('income-value')?.dataset.value  || 0);
  const expense = Number(document.getElementById('expense-value')?.dataset.value || 0);

  // ── Income vs Expense doughnut ──────────────────────────
  const ctx1 = document.getElementById('incomeExpenseChart');
  if (ctx1 && (income > 0 || expense > 0)) {
    new Chart(ctx1, {
      type: 'doughnut',
      data: {
        labels: ['Income', 'Expense'],
        datasets: [{
          data: [income, expense],
          backgroundColor: ['#1E8449', '#C0392B'],
          borderWidth: 2,
          borderColor: '#fff'
        }]
      },
      options: {
        cutout: '65%',
        responsive: true,
        maintainAspectRatio: true,
        plugins: { legend: { position: 'bottom' } }
      }
    });
  } else if (ctx1) {
    // No data — show placeholder text on canvas
    const ctx = ctx1.getContext('2d');
    ctx1.height = 200;
    ctx.fillStyle = '#aaa';
    ctx.font = '14px Outfit, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('No transactions yet', ctx1.width / 2, 100);
  }

  // ── Spending by Category doughnut ───────────────────────
  const ctx2 = document.getElementById('expenseCategoryChart');
  if (ctx2) {
    fetch('/api/category-summary/')
      .then(r => r.json())
      .then(({ categories }) => {
        if (!categories || !categories.length) {
          const ctx = ctx2.getContext('2d');
          ctx.fillStyle = '#aaa';
          ctx.font = '14px Outfit, sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText('No expense data yet', ctx2.width / 2, 100);
          return;
        }
        new Chart(ctx2, {
          type: 'doughnut',
          data: {
            labels: categories.map(c => c.label),
            datasets: [{
              data: categories.map(c => c.value),
              backgroundColor: [
                '#0A3D62','#1E8449','#C0392B','#F39C12',
                '#8E44AD','#16A085','#2980B9','#D35400'
              ],
              borderWidth: 2,
              borderColor: '#fff'
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: { legend: { position: 'bottom' } }
          }
        });
      })
      .catch(() => {});
  }
}

// Run after DOM + Chart.js are both ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initDashboardCharts);
} else {
  initDashboardCharts();
}
