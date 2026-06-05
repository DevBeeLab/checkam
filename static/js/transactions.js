// ── transactions.js ────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {

  // ── Add Transaction button ─────────────────────────────
  document.getElementById('addTransactionBtn')?.addEventListener('click', () => {
    window.openModal('addTransaction');
  });

  // ── Edit Transaction — wire both table rows and mobile cards ──
  function wireEditButtons(container) {
    container.querySelectorAll('.edit-transaction').forEach(btn => {
      btn.addEventListener('click', () => {
        const { id, description, amount, category } = btn.dataset;
        const transaction_type = btn.dataset.transaction_type;

        const form = document.getElementById('editTransactionForm');
        form.action = `/edit-transaction/${id}`;
        form.querySelector('#edit_txn_description').value = description || '';
        form.querySelector('#edit_txn_amount').value      = amount     || '';

        const typeEl = form.querySelector('#edit_txn_type');
        if (typeEl) typeEl.value = transaction_type || 'income';

        const catEl = form.querySelector('#edit_txn_category');
        if (catEl) catEl.value = category || 'other';

        window.openModal('editTransaction');
      });
    });
  }

  wireEditButtons(document);

  // ── Filter / Search / Sort / Pagination ───────────────
  const searchInput    = document.getElementById('searchInput');
  const typeFilter     = document.getElementById('typeFilter');
  const categoryFilter = document.getElementById('categoryFilter');
  const sortFilter     = document.getElementById('sortFilter');
  const tbody          = document.getElementById('transactions-body');
  const cardContainer  = document.getElementById('txn-cards-mobile');

  if (!tbody) return;

  // Snapshot all rows AND cards once — never destroy them
  const allRows  = Array.from(tbody.querySelectorAll('tr[data-id]'));
  const allCards = cardContainer
    ? Array.from(cardContainer.querySelectorAll('.txn-card[data-id]'))
    : [];

  // Populate category dropdown
  if (categoryFilter) {
    const seen = new Set();
    allRows.forEach(r => {
      const cat = r.dataset.category;
      if (cat && !seen.has(cat)) {
        seen.add(cat);
        const opt = document.createElement('option');
        opt.value = cat;
        opt.textContent = cat.charAt(0).toUpperCase() + cat.slice(1);
        categoryFilter.appendChild(opt);
      }
    });
  }

  const PAGE_SIZE = 10;
  let currentPage = 1;

  function getFiltered() {
    const search   = (searchInput?.value    || '').toLowerCase().trim();
    const type     = (typeFilter?.value     || '').toLowerCase();
    const category = (categoryFilter?.value || '').toLowerCase();
    const sort     = sortFilter?.value || 'date_desc';

    // Filter using table rows as source of truth
    let rows = allRows.filter(row => {
      const desc    = (row.dataset.description || '').toLowerCase();
      const rowType = (row.dataset.type        || '').toLowerCase();
      const rowCat  = (row.dataset.category    || '').toLowerCase();
      return (!search   || desc.includes(search))
          && (!type     || rowType === type)
          && (!category || rowCat  === category);
    });

    rows.sort((a, b) => {
      switch (sort) {
        case 'date_asc':    return new Date(a.dataset.date)    - new Date(b.dataset.date);
        case 'amount_desc': return parseFloat(b.dataset.amount) - parseFloat(a.dataset.amount);
        case 'amount_asc':  return parseFloat(a.dataset.amount) - parseFloat(b.dataset.amount);
        default:            return new Date(b.dataset.date)    - new Date(a.dataset.date);
      }
    });

    return rows;
  }

  function render() {
    const rows  = getFiltered();
    const start = (currentPage - 1) * PAGE_SIZE;
    const page  = rows.slice(start, start + PAGE_SIZE);

    // Collect IDs on current page
    const visibleIds = new Set(page.map(r => r.dataset.id));

    // ── Table rows ──
    const emptyRow = document.getElementById('empty-row');
    emptyRow?.remove();

    allRows.forEach(r => { r.style.display = 'none'; });

    if (!page.length) {
      const tr = document.createElement('tr');
      tr.id = 'empty-row';
      tr.innerHTML = '<td colspan="6" class="text-center empty-cell">No transactions found.</td>';
      tbody.appendChild(tr);
    } else {
      page.forEach(r => { tbody.appendChild(r); r.style.display = ''; });
    }

    // ── Mobile cards — show/hide by matching ID ──
    allCards.forEach(card => {
      card.style.display = visibleIds.has(card.dataset.id) ? '' : 'none';
    });

    renderPagination(rows.length);
  }

  function renderPagination(total) {
    const container = document.getElementById('paginationContainer');
    if (!container) return;
    container.innerHTML = '';
    const pages = Math.ceil(total / PAGE_SIZE);
    if (pages <= 1) return;

    for (let i = 1; i <= pages; i++) {
      const btn = document.createElement('button');
      btn.textContent = i;
      btn.className   = 'pagination-btn' + (i === currentPage ? ' active' : '');
      btn.addEventListener('click', () => { currentPage = i; render(); });
      container.appendChild(btn);
    }
  }

  function resetAndRender() { currentPage = 1; render(); }

  [searchInput, typeFilter, categoryFilter, sortFilter].forEach(el => {
    el?.addEventListener('input',  resetAndRender);
    el?.addEventListener('change', resetAndRender);
  });

  render();
});