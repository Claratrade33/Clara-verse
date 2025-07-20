document.addEventListener("DOMContentLoaded", () => {
  fetchDados();

  setInterval(fetchDados, 15000); // Atualiza a cada 15s

  window.enviarAcao = (acao) => {
    fetch(`/executar/${acao}`, {
      method: "POST"
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById("mensagemStatus").innerText = data.mensagem;
      if (data.saldo !== undefined) {
        document.getElementById("saldo").innerText = data.saldo;
      }
    });
  };
});

function fetchDados() {
  fetch("/dados_mercado")
    .then(res => res.json())
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