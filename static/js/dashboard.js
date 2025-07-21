// Atualiza os dados do mercado automaticamente
function atualizarDadosMercado() {
  fetch("/dados_mercado")
    .then(response => response.json())
    .then(data => {
      document.getElementById("preco").innerText = data.preco;
      document.getElementById("variacao").innerText = data.variacao;
      document.getElementById("volume").innerText = data.volume;
      document.getElementById("rsi").innerText = data.rsi;
      document.getElementById("suporte").innerText = data.suporte;
      document.getElementById("resistencia").innerText = data.resistencia;
      document.getElementById("sugestao").innerText = data.sugestao;
    });
}

if (window.location.pathname === "/painel") {
  atualizarDadosMercado();
  setInterval(atualizarDadosMercado, 10000);
}

// Envia uma ação de trading (entrada, stop, etc)
function enviarAcao(acao) {
  fetch(`/executar/${acao}`, {
    method: "POST"
  })
    .then(response => response.json())
    .then(data => {
      const status = document.getElementById("mensagemStatus");
      status.innerText = data.mensagem;
      status.style.display = "block";
      setTimeout(() => status.style.display = "none", 5000);
    });
}

// Salva as chaves da API
function salvarChaves() {
  const binance_api_key = document.getElementById("binance_api_key").value;
  const binance_api_secret = document.getElementById("binance_api_secret").value;
  const openai_api_key = document.getElementById("openai_api_key").value;

  fetch("/salvar_chaves", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      binance_api_key,
      binance_api_secret,
      openai_api_key
    })
  })
    .then(response => response.json())
    .then(data => {
      if (data.status === "sucesso") {
        document.getElementById("status-chaves").innerText = "✅ Chaves salvas com sucesso!";
        setTimeout(() => {
          window.location.href = "/painel";
        }, 1500);
      } else {
        document.getElementById("status-chaves").innerText = "❌ Erro ao salvar chaves.";
      }
    });
}

// Atualização contínua mesmo após o carregamento
document.addEventListener("DOMContentLoaded", function () {
  if (window.location.pathname === "/painel") {
    atualizarDadosMercado();
    setInterval(atualizarDadosMercado, 10000);
  }
});