async function salvarChaves() {
  const dados = {
    binance_api_key: document.getElementById("binance_api_key").value,
    binance_api_secret: document.getElementById("binance_api_secret").value,
    openai_api_key: document.getElementById("openai_api_key").value,
  };

  const r = await fetch("/salvar_chaves", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados)
  });

  const res = await r.json();
  if (res.status === "sucesso") {
    window.location.href = res.redirect;
  } else {
    alert("Erro ao salvar chaves: " + res.mensagem);
  }
}

async function carregarDadosMercado() {
  const r = await fetch("/dados_mercado");
  const d = await r.json();
  document.getElementById("preco").innerText = d.preco;
  document.getElementById("variacao").innerText = d.variacao;
  document.getElementById("volume").innerText = d.volume;
  document.getElementById("rsi").innerText = d.rsi;
  document.getElementById("suporte").innerText = d.suporte;
  document.getElementById("resistencia").innerText = d.resistencia;
  document.getElementById("sugestao").innerText = d.sugestao;
}

async function enviarAcao(acao) {
  const r = await fetch(`/executar/${acao}`, { method: "POST" });
  const d = await r.json();
  document.getElementById("mensagemStatus").innerText = d.mensagem;
}

setInterval(carregarDadosMercado, 6000);
window.onload = carregarDadosMercado;