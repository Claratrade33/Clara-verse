// Atualiza os dados do mercado
async function atualizarDados() {
  const resposta = await fetch("/dados_mercado");
  const dados = await resposta.json();

  document.getElementById("preco").innerText = dados.preco;
  document.getElementById("variacao").innerText = dados.variacao;
  document.getElementById("volume").innerText = dados.volume;
  document.getElementById("rsi").innerText = dados.rsi;
  document.getElementById("suporte").innerText = dados.suporte;
  document.getElementById("resistencia").innerText = dados.resistencia;
  document.getElementById("sugestao").innerText = dados.sugestao;
}

// Envia comandos como entrada, stop, alvo...
async function enviarAcao(acao) {
  const resposta = await fetch(`/executar/${acao}`, {
    method: "POST"
  });
  const resultado = await resposta.json();
  const status = document.getElementById("mensagemStatus");
  status.innerText = resultado.mensagem;
  setTimeout(() => {
    status.innerText = "";
  }, 3000);
}

// Salva as chaves de API com redirecionamento para o painel
async function salvarChaves() {
  const binanceKey = document.getElementById("binance_api_key").value;
  const binanceSecret = document.getElementById("binance_api_secret").value;
  const openaiKey = document.getElementById("openai_api_key").value;

  const resposta = await fetch("/salvar_chaves", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      binance_api_key: binanceKey,
      binance_api_secret: binanceSecret,
      openai_api_key: openaiKey
    })
  });

  const resultado = await resposta.json();

  const status = document.getElementById("status-chaves");
  if (resultado.status === "sucesso") {
    status.innerText = "🔒 Chaves salvas com sucesso!";
    setTimeout(() => {
      window.location.href = "/painel";
    }, 1200);
  } else {
    status.innerText = "❌ Erro ao salvar as chaves.";
  }
}

// Atualizar mercado automaticamente a cada 10 segundos
setInterval(atualizarDados, 10000);
window.onload = atualizarDados;