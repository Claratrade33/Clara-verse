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
    })
    .catch(() => {
      document.getElementById("sugestao").innerText = "Erro ao obter dados.";
    });
}

// Chama a função de atualização assim que a página carrega
if (window.location.pathname === "/painel") {
  atualizarDadosMercado();
  setInterval(atualizarDadosMercado, 10000); // Atualiza a cada 10 segundos
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
      setTimeout(() => status.style.display = "none", 4000);
    })
    .catch(() => {
      alert("Erro ao enviar ação.");
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
      const status = document.getElementById("status-chaves");
      if (data.status === "sucesso") {
        status.innerText = "🔐 Chaves salvas com sucesso!";
        status.style.color = "lightgreen";
        setTimeout(() => {
          window.location.href = "/painel";
        }, 1500);
      } else {
        status.innerText = "❌ Erro ao salvar: " + data.mensagem;
        status.style.color = "red";
      }
    })
    .catch(() => {
      const status = document.getElementById("status-chaves");
      status.innerText = "❌ Erro ao salvar as chaves.";
      status.style.color = "red";
    });
}