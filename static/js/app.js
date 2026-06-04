// Apply saved theme on every page load
(function () {
  const theme = localStorage.getItem('checkam_theme') || 'light';
  if (theme === 'dark') document.body.classList.add('dark-mode');
})();
