// Atualiza dados de mercado BTC/USDT a cada 5 segundos
function atualizarDadosMercado() {
  fetch("/dados_mercado?par=BTCUSDT")
    .then(response => response.json())
    .then(data => {
      document.getElementById("preco").textContent = data.preco;
      document.getElementById("variacao").textContent = data.variacao;
      document.getElementById("volume").textContent = data.volume;
    })
    .catch(() => {
      document.getElementById("preco").textContent = "--";
      document.getElementById("variacao").textContent = "--";
      document.getElementById("volume").textContent = "--";
    });
}

setInterval(atualizarDadosMercado, 5000);
atualizarDadosMercado();

// Inicializa gráfico com dados fictícios (pode integrar WebSocket depois)
let ctx = document.getElementById("graficoBTC").getContext("2d");
let graficoBTC = new Chart(ctx, {
  type: 'line',
  data: {
    labels: Array.from({ length: 30 }, (_, i) => i + 1),
    datasets: [{
      label: "BTC/USDT",
      data: Array.from({ length: 30 }, () => Math.random() * 10000 + 20000),
      borderWidth: 2,
      fill: false,
      tension: 0.4
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: false
      }
    }
  }
});

// Modal de Configurações
function abrirConfiguracoes() {
  document.getElementById("modal-config").style.display = "block";
}

function fecharConfiguracoes() {
  document.getElementById("modal-config").style.display = "none";
}

function salvarChaves() {
  const apiKey = document.getElementById("binance_api_key").value;
  const apiSecret = document.getElementById("binance_api_secret").value;
  const openaiKey = document.getElementById("openai_api_key").value;

  fetch("/salvar_chaves", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      binance_api_key: apiKey,
      binance_api_secret: apiSecret,
      openai_api_key: openaiKey
    })
  })
    .then(res => res.json())
    .then(res => {
      alert("Chaves salvas com sucesso!");
      fecharConfiguracoes();
    })
    .catch(() => {
      alert("Erro ao salvar chaves.");
    });
}

// Comandos simulados
function acao(tipo) {
  alert(`Comando enviado: ${tipo.toUpperCase()}`);
}