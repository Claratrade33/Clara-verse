document.addEventListener("DOMContentLoaded", () => {
  atualizarDadosMercado();

  const acaoBotoes = ["entrada", "stop", "alvo", "executar", "automatico"];
  acaoBotoes.forEach((acao) => {
    const botao = document.querySelector(`button[onclick*="${acao}"]`);
    if (botao) {
      botao.addEventListener("click", () => enviarAcao(acao));
    }
  });

  const btnSalvar = document.querySelector("button[onclick='salvarChaves()']");
  if (btnSalvar) {
    btnSalvar.addEventListener("click", salvarChaves);
  }
});

function atualizarDadosMercado() {
  fetch("/dados_mercado")
    .then((res) => res.json())
    .then((dados) => {
      document.getElementById("preco").textContent = dados.preco;
      document.getElementById("variacao").textContent = dados.variacao;
      document.getElementById("volume").textContent = dados.volume;
      document.getElementById("rsi").textContent = dados.rsi;
      document.getElementById("suporte").textContent = dados.suporte;
      document.getElementById("resistencia").textContent = dados.resistencia;
      document.getElementById("sugestao").textContent = dados.sugestao;
    })
    .catch(() => {
      document.getElementById("sugestao").textContent = "Erro ao buscar dados.";
    });
}

function enviarAcao(acao) {
  fetch(`/executar/${acao}`, { method: "POST" })
    .then((res) => res.json())
    .then((dados) => {
      document.getElementById("mensagemStatus").textContent = dados.mensagem;
    })
    .catch(() => {
      document.getElementById("mensagemStatus").textContent =
        "Erro ao executar ação.";
    });
}

function salvarChaves() {
  const binance_api_key = document.getElementById("binance_api_key")?.value || "";
  const binance_api_secret = document.getElementById("binance_api_secret")?.value || "";
  const openai_api_key = document.getElementById("openai_api_key")?.value || "";

  fetch("/salvar_chaves", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      binance_api_key,
      binance_api_secret,
      openai_api_key,
    }),
  })
    .then((res) => res.json())
    .then(() => {
      document.getElementById("mensagemStatus").textContent =
        "🔒 Chaves salvas com sucesso!";
      setTimeout(() => {
        window.location.href = "/painel";
      }, 1500);
    })
    .catch(() => {
      document.getElementById("mensagemStatus").textContent =
        "Erro ao salvar as chaves.";
    });
}