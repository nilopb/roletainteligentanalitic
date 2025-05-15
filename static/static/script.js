// Script geral

// Ativar/Desativar modo noturno e salvar no localStorage
document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.getElementById('toggle-dark-mode');
  if (!toggleBtn) return;

  // Aplica tema salvo
  if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
  }

  toggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
  });
});
