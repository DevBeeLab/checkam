// ── app.js ──────────────────────────────────────────────────

// Apply saved theme on every page load
(function () {
  const theme = localStorage.getItem('checkam_theme') || 'light';
  if (theme === 'dark') document.body.classList.add('dark-mode');
})();

// Mobile sidebar toggle
document.addEventListener('DOMContentLoaded', () => {
  const toggle  = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.sidebar');
  if (!toggle || !sidebar) return;

  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });

  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', (e) => {
    if (window.innerWidth <= 900
        && !sidebar.contains(e.target)
        && !toggle.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
});