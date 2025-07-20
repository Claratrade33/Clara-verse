document.addEventListener("DOMContentLoaded", () => {
    atualizarDados();

    setInterval(atualizarDados, 10000); // Atualiza mercado a cada 10s

    document.getElementById("btnEntrada")?.addEventListener("click", () => executarAcao("entrada"));
    document.getElementById("btnStop")?.addEventListener("click", () => executarAcao("stop"));
    document.getElementById("btnAlvo")?.addEventListener("click", () => executarAcao("alvo"));
    document.getElementById("btnAuto")?.addEventListener("click", () => executarAcao("automatico"));
    document.getElementById("btnExecutar")?.addEventListener("click", () => executarAcao("executar"));
    document.getElementById("btnSalvar")?.addEventListener("click", salvarChaves);
});

function atualizarDados() {
    fetch("/dados_mercado")
        .then(res => res.json())
        .then(data => {
            document.getElementById("preco").textContent = data.preco || "--";
            document.getElementById("variacao").textContent = data.variacao || "--";
            document.getElementById("volume").textContent = data.volume || "--";
            document.getElementById("rsi")?.textContent = data.rsi || "--";
            document.getElementById("suporte")?.textContent = data.suporte || "--";
            document.getElementById("resistencia")?.textContent = data.resistencia || "--";
            document.getElementById("sugestao")?.textContent = data.sugestao || "--";
        });
}

function executarAcao(acao) {
    fetch(`/executar/${acao}`, {
        method: "POST"
    })
        .then(res => res.json())
        .then(data => {
            alert(data.mensagem);
        });
}

function salvarChaves() {
    const binanceKey = document.getElementById("binance_api_key")?.value;
    const binanceSecret = document.getElementById("binance_api_secret")?.value;
    const openaiKey = document.getElementById("openai_api_key")?.value;

    fetch("/salvar_chaves", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            binance_api_key: binanceKey,
            binance_api_secret: binanceSecret,
            openai_api_key: openaiKey
        })
    })
        .then(res => res.json())
        .then(data => {
            const status = document.getElementById("status-chaves");
            if (status) {
                status.textContent = "🔒 Chaves salvas com sucesso!";
                setTimeout(() => status.textContent = "", 3000);
            }
        });
}