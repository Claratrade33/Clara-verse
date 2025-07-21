// dashboard.js

// Função para salvar as chaves da API
function salvarChaves() {
  const binanceApiKey = document.getElementById("binance_api_key").value;
  const binanceApiSecret = document.getElementById("binance_api_secret").value;
  const openaiApiKey = document.getElementById("openai_api_key").value;

  fetch("/salvar_chaves", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      binance_api_key: binanceApiKey,
      binance_api_secret: binanceApiSecret,
      openai_api_key: openaiApiKey
    })
  })
    .then(response => response.json())
    .then(data => {
      const status = document.getElementById("status-chaves");
      if (data.status === "sucesso") {
        status.textContent = "🔐 Chaves salvas com sucesso!";
        status.style.color = "limegreen";
        setTimeout(() => {
          window.location.href = "/painel";
        }, 1000); // Redireciona após 1s
      } else {
        status.textContent = "❌ Erro ao salvar as chaves.";
        status.style.color = "red";
      }
    })
    .catch(err => {
      console.error("Erro ao salvar:", err);
      const status = document.getElementById("status-chaves");
      status.textContent = "❌ Erro de conexão.";
      status.style.color = "red";
    });
}

// Enviar comandos do painel
function enviarAcao(acao) {
  fetch(`/executar/${acao}`, {
    method: "POST"
  })
    .then(response => response.json())
    .then(data => {
      const msg = document.getElementById("mensagemStatus");
      msg.textContent = data.mensagem;
      msg.style.color = "aqua";
      setTimeout(() => {
        msg.textContent = "";
      }, 4000);
    })
    .catch(error => {
      console.error("Erro ao enviar comando:", error);
    });
}

// Carregar dados de mercado no painel
function carregarDadosMercado() {
  fetch("/dados_mercado")
    .then(response => response.json())
    .then(data => {
      document.getElementById("preco").textContent = data.preco;
      document.getElementById("variacao").textContent = data.variacao;
      document.getElementById("volume").textContent = data.volume;
      document.getElementById("rsi").textContent = data.rsi;
      document.getElementById("suporte").textContent = data.suporte;
      document.getElementById("resistencia").textContent = data.resistencia;
      document.getElementById("sugestao").textContent = data.sugestao;
    })
    .catch(error => {
      console.error("Erro ao carregar dados:", error);
    });
}

// Inicia carregamento quando entra no painel
if (window.location.pathname === "/painel") {
  setInterval(carregarDadosMercado, 5000);
  carregarDadosMercado();
}