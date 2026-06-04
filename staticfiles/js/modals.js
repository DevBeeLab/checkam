// ── modals.js ──────────────────────────────────────────────
window.openModal = function (modalName) {
  const modal = document.getElementById(`${modalName}Modal`);
  if (!modal) return;
  modal.classList.remove('modal--hidden');
  modal.setAttribute('aria-hidden', 'false');
};

window.closeModal = function (modalName) {
  const modal = document.getElementById(`${modalName}Modal`);
  if (!modal) return;
  modal.classList.add('modal--hidden');
  modal.setAttribute('aria-hidden', 'true');
};

document.addEventListener('click', function (e) {
  // Close/Cancel buttons
  const closeBtn = e.target.closest('[data-modal-close]');
  if (closeBtn) {
    window.closeModal(closeBtn.getAttribute('data-modal-close'));
  }
  // Overlay click
  if (e.target.classList.contains('modal') && e.target.dataset.closeOnOverlay === 'true') {
    e.target.classList.add('modal--hidden');
    e.target.setAttribute('aria-hidden', 'true');
  }
});

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    const open = document.querySelector('.modal:not(.modal--hidden)');
    if (open) { open.classList.add('modal--hidden'); open.setAttribute('aria-hidden', 'true'); }
  }
});
