document.addEventListener("DOMContentLoaded", function () {
  const saldoDisplay = document.getElementById("saldo");
  const precoBTC = document.getElementById("preco-btc");
  const respostaIA = document.getElementById("resposta-ia");

  function atualizarSaldo() {
    fetch("/obter_saldo")
      .then(res => res.json())
      .then(data => {
        saldoDisplay.textContent = `$${parseFloat(data.saldo).toFixed(2)}`;
      });
  }

  function atualizarPreco() {
    fetch("/obter_preco")
      .then(res => res.json())
      .then(data => {
        precoBTC.textContent = parseFloat(data.preco).toFixed(2) + " USDT";
      });
  }

  function executarAcao(acao) {
    fetch("/executar_acao", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ acao })
    })
    .then(res => res.json())
    .then(data => {
      respostaIA.textContent = data.mensagem;
      atualizarSaldo();
    });
  }

  // Botões
  document.getElementById("btnComprar").addEventListener("click", () => executarAcao("comprar"));
  document.getElementById("btnVender").addEventListener("click", () => executarAcao("vender"));
  document.getElementById("btnAuto").addEventListener("click", () => executarAcao("auto"));

  document.getElementById("btnIA").addEventListener("click", () => {
    respostaIA.textContent = "Consultando Clarinha...";
    fetch("/obter_sugestao_ia")
      .then(res => res.json())
      .then(data => {
        respostaIA.textContent = data.resposta || "IA indisponível.";
      });
  });

  atualizarPreco();
  atualizarSaldo();
  setInterval(atualizarPreco, 10000);
});