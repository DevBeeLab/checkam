// ── budgets.js ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {

  // ── Add Budget ─────────────────────────────────────────
  document.getElementById('addBudgetBtn')?.addEventListener('click', () => {
    window.openModal('addBudget');
  });

  // ── Edit Budget ────────────────────────────────────────
  document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const { id, category, limit } = btn.dataset;

      document.getElementById('edit_category').value = category || '';
      document.getElementById('edit_limit').value    = limit    || '';
      document.getElementById('editBudgetForm').action = `/edit-budget/${id}`;

      window.openModal('editBudget');
    });
  });

});
