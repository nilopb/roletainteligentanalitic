document.addEventListener('DOMContentLoaded', () => {
  // Modo noturno toggle
  const toggleBtn = document.getElementById('darkModeToggle');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      document.body.classList.toggle('dark-mode');
      localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
    });
    // Inicializa modo noturno salvo
    if (localStorage.getItem('darkMode') === 'true') {
      document.body.classList.add('dark-mode');
    }
  }

  // Gráfico de palpites com Chart.js
  const ctx = document.getElementById('chartPredictions');
  if (ctx) {
    fetch('/get_predictions_data')
      .then(res => res.json())
      .then(data => {
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: [{
              label: 'Probabilidade (%)',
              data: data.values,
              backgroundColor: 'rgba(0, 255, 204, 0.7)',
              borderColor: 'rgba(0, 255, 204, 1)',
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
                max: 100
              }
            },
            plugins: {
              legend: {
                labels: {
                  color: '#00ffcc',
                  font: { size: 16 }
                }
              }
            }
          }
        });
      });
  }

  // Função para simulação de apostas
  const simulateBtn = document.getElementById('simulateBet');
  if (simulateBtn) {
    simulateBtn.addEventListener('click', () => {
      const numInput = document.getElementById('betNumbers');
      const valueInput = document.getElementById('betValue');
      const resultDiv = document.getElementById('simulationResult');
      const numbers = numInput.value.split(',').map(n => parseInt(n.trim())).filter(n => !isNaN(n));
      const betValue = parseFloat(valueInput.value);
      if (numbers.length === 0 || isNaN(betValue) || betValue <= 0) {
        resultDiv.textContent = 'Por favor, insira números válidos e valor maior que zero.';
        return;
      }
      // Simulação básica: chance de ganhar 1 em 37 por número apostado
      const chance = 1 - Math.pow(36/37, numbers.length);
      const expectedReturn = betValue * chance * 36; // pagamento típico da roleta
      resultDiv.textContent = `Chance aproximada de ganhar: ${(chance*100).toFixed(2)}%. Retorno esperado: R$ ${expectedReturn.toFixed(2)}.`;
    });
  }
});
