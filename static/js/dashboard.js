document.addEventListener("DOMContentLoaded", () => {
    atualizarDadosMercado();
    setInterval(atualizarDadosMercado, 10000); // atualiza a cada 10s
});

function atualizarDadosMercado() {
    fetch("/dados_mercado")
        .then(response => response.json())
        .then(data => {
            document.getElementById("preco").innerText = data.preco;
            document.getElementById("variacao").innerText = data.variacao;
            document.getElementById("volume").innerText = data.volume;
        })
        .catch(error => console.error("Erro ao buscar dados do mercado:", error));
}

function salvarChaves() {
    const binanceKey = document.getElementById("binance_api_key").value;
    const binanceSecret = document.getElementById("binance_api_secret").value;
    const openaiKey = document.getElementById("openai_api_key").value;

    fetch("/salvar_chaves", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            binance_api_key: binanceKey,
            binance_api_secret: binanceSecret,
            openai_api_key: openaiKey
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "sucesso") {
            document.getElementById("status-chaves").innerText = "✅ Chaves salvas com sucesso!";
        }
    })
    .catch(error => {
        document.getElementById("status-chaves").innerText = "❌ Erro ao salvar chaves!";
        console.error("Erro ao salvar chaves:", error);
    });
}

function enviarComando(tipo) {
    fetch(`/comando?acao=${tipo}`)
        .then(response => response.json())
        .then(data => {
            alert(`📡 Comando "${tipo}" enviado!\nIA: ${data.mensagem}`);
        })
        .catch(error => {
            alert(`❌ Erro ao enviar comando "${tipo}"`);
            console.error(error);
        });
}