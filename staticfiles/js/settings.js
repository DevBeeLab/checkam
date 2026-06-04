document.addEventListener('DOMContentLoaded', () => {
  const themeSelect = document.getElementById('themeSelect');
  const preferencesForm = document.getElementById('preferencesForm');

  // Load saved theme
  const savedTheme = localStorage.getItem('checkam_theme') || 'light';
  if (themeSelect) themeSelect.value = savedTheme;
  document.body.classList.toggle('dark-mode', savedTheme === 'dark');

  preferencesForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    const theme = themeSelect?.value || 'light';
    localStorage.setItem('checkam_theme', theme);
    document.body.classList.toggle('dark-mode', theme === 'dark');
    // Show feedback
    const btn = preferencesForm.querySelector('[type="submit"]');
    const orig = btn.textContent;
    btn.textContent = 'Saved!';
    setTimeout(() => { btn.textContent = orig; }, 1500);
  });
});
