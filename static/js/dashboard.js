document.addEventListener("DOMContentLoaded", () => {
  atualizarMercado();

  const intervalo = setInterval(atualizarMercado, 10000);
});

function atualizarMercado() {
  fetch("/dados_mercado?par=BTCUSDT")
    .then(res => res.json())
    .then(data => {
      document.getElementById("preco").innerText = data.preco || "--";
      document.getElementById("variacao").innerText = data.variacao || "--";
      document.getElementById("volume").innerText = data.volume || "--";
    })
    .catch(() => console.warn("Erro ao buscar dados do mercado"));
}

function salvarChaves() {
  const binance_api_key = document.getElementById("binance_api_key").value;
  const binance_api_secret = document.getElementById("binance_api_secret").value;
  const openai_api_key = document.getElementById("openai_api_key").value;

  fetch("/salvar_chaves", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ binance_api_key, binance_api_secret, openai_api_key })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("status-chaves").innerText = "Chaves salvas com sucesso!";
    setTimeout(() => {
      document.getElementById("status-chaves").innerText = "";
    }, 3000);
  });
}

function executarAcao(acao) {
  fetch(`/executar_acao?comando=${acao}`)
    .then(res => res.json())
    .then(data => {
      const sugestao = document.getElementById("sugestao");
      if (sugestao) sugestao.innerText = data.resposta || "Sem resposta da IA.";
    });
}