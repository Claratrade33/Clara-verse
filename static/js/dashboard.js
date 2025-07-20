document.addEventListener("DOMContentLoaded", () => {
    atualizarMercado();

    // Atualiza mercado a cada 15s
    setInterval(atualizarMercado, 15000);
});

function atualizarMercado() {
    fetch("/dados_mercado")
        .then(res => res.json())
        .then(data => {
            document.getElementById("preco").textContent = data.preco || "--";
            document.getElementById("variacao").textContent = data.variacao || "--";
            document.getElementById("volume").textContent = data.volume || "--";
        });
}

function salvarChaves() {
    const binance_api_key = document.getElementById("binance_api_key").value;
    const binance_api_secret = document.getElementById("binance_api_secret").value;
    const openai_api_key = document.getElementById("openai_api_key").value;

    fetch("/salvar_chaves", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            binance_api_key,
            binance_api_secret,
            openai_api_key
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("status-chaves").textContent = "✅ Chaves salvas com sucesso!";
        setTimeout(() => {
            document.getElementById("status-chaves").textContent = "";
        }, 3000);
    });
}

function enviarComando(tipo) {
    fetch(`/executar_ia?tipo=${tipo}`)
        .then(res => res.json())
        .then(data => {
            alert(`📊 IA responde:
            
• Entrada: ${data.entrada}
• Alvo: ${data.alvo}
• Stop: ${data.stop}
• Confiança: ${data.confianca}`);
        })
        .catch(() => {
            alert("Erro ao processar comando da IA.");
        });
}