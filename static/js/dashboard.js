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

    atualizarSaldo();
    atualizarPreco();
    setInterval(atualizarPreco, 10000);
});