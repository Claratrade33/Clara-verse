document.addEventListener("DOMContentLoaded", function () {
  const respostaIA = document.getElementById("resposta-ia");
  const saldoDisplay = document.getElementById("saldo");
  const precoBTC = document.getElementById("preco-btc");

  function atualizarSaldo() {
    fetch("/obter_saldo")
      .then(res => res.json())
      .then(data => {
        saldoDisplay.textContent = data.saldo.toFixed(2) + " USDT";
      });
  }

  function atualizarPreco() {
    fetch("/obter_preco")
      .then(res => res.json())
      .then(data => {
        precoBTC.textContent = parseFloat(data.preco).toFixed(2) + " USDT";
      });
  }

  function acaoBotao(acao) {
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
  document.getElementById("btnEntrada").addEventListener("click", () => acaoBotao("entrada"));
  document.getElementById("btnStop").addEventListener("click", () => acaoBotao("stop"));
  document.getElementById("btnAlvo").addEventListener("click", () => acaoBotao("alvo"));
  document.getElementById("btnAuto").addEventListener("click", () => acaoBotao("auto"));
  document.getElementById("btnExecutar").addEventListener("click", () => acaoBotao("executar"));

  document.getElementById("btnIA").addEventListener("click", () => {
    respostaIA.textContent = "Analisando com a IA...";
    fetch("/obter_sugestao_ia")
      .then(res => res.json())
      .then(data => {
        respostaIA.textContent = data.resposta;
      });
  });

  // 📊 Análise Técnica usando API pública da Binance
  function carregarAnaliseTecnica() {
    fetch("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=100")
      .then(res => res.json())
      .then(velas => {
        const fechamentos = velas.map(v => parseFloat(v[4]));
        const min = Math.min(...fechamentos);
        const max = Math.max(...fechamentos);
        const media = fechamentos.reduce((a, b) => a + b, 0) / fechamentos.length;
        const precoAtual = fechamentos[fechamentos.length - 1];

        // RSI (período 14)
        const ganhos = [];
        const perdas = [];
        for (let i = 1; i <= 14; i++) {
          const dif = fechamentos[i] - fechamentos[i - 1];
          if (dif >= 0) ganhos.push(dif);
          else perdas.push(Math.abs(dif));
        }
        const mediaGanhos = ganhos.reduce((a, b) => a + b, 0) / 14;
        const mediaPerdas = perdas.reduce((a, b) => a + b, 0) / 14;
        const rsi = 100 - (100 / (1 + (mediaGanhos / mediaPerdas || 1)));

        const tendencia = precoAtual > media ? "Alta" : "Baixa";

        // Preenche na tela
        document.querySelector(".painel-binance ul").innerHTML = `
          <li>🧠 RSI atual: <strong>${rsi.toFixed(2)}</strong></li>
          <li>📉 Suporte: <strong>${min.toFixed(2)}</strong></li>
          <li>📈 Resistência: <strong>${max.toFixed(2)}</strong></li>
          <li>📊 Tendência: <strong>${tendencia}</strong></li>
        `;
      });
  }

  atualizarSaldo();
  atualizarPreco();
  carregarAnaliseTecnica();
  setInterval(atualizarPreco, 10000);
});