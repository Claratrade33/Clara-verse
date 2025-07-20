document.addEventListener("DOMContentLoaded", () => {
  atualizarDadosMercado();
  setInterval(atualizarDadosMercado, 15000); // atualiza a cada 15s
});

function atualizarDadosMercado() {
  fetch("/dados_mercado")
    .then(res => res.json())
    .then(data => {
      if (document.getElementById("preco")) {
        document.getElementById("preco").textContent = data.preco;
        document.getElementById("variacao").textContent = data.variacao;
        document.getElementById("volume").textContent = data.volume;
        document.getElementById("rsi").textContent = data.rsi;
        document.getElementById("suporte").textContent = data.suporte;
        document.getElementById("resistencia").textContent = data.resistencia;
        document.getElementById("sugestao").textContent = data.sugestao;
      }
    })
    .catch(() => {
      console.log("Erro ao atualizar dados de mercado.");
    });
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
  .then(data => {
    if (data.status === "sucesso") {
      document.getElementById("status-chaves").textContent = "✅ Chaves salvas com sucesso!";
      setTimeout(() => {
        document.getElementById("status-chaves").textContent = "";
      }, 3000);
    }
  })
  .catch(() => {
    document.getElementById("status-chaves").textContent = "❌ Erro ao salvar chaves.";
  });
}

function enviarComando(acao) {
  fetch(`/executar/${acao}`, {
    method: "POST"
  })
  .then(res => res.json())
  .then(data => {
    alert(`🚀 ${data.mensagem}`);
  })
  .catch(() => {
    alert("❌ Erro ao enviar comando.");
  });
}