async function salvarChaves() {
    const binanceKey = document.getElementById("binance_key").value;
    const binanceSecret = document.getElementById("binance_secret").value;
    const openaiKey = document.getElementById("openai_key").value;

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
    if (resultado.status === "sucesso") {
        alert("🔐 Chaves salvas com sucesso!");
    } else {
        alert("⚠️ Erro ao salvar chaves.");
    }
}

async function carregarDadosMercado() {
    const resposta = await fetch("/dados_mercado");
    const dados = await resposta.json();
    document.getElementById("preco").innerText = `R$ ${dados.preco}`;
    document.getElementById("variacao").innerText = `${dados.variacao}%`;
    document.getElementById("volume").innerText = `${dados.volume}`;
}

setInterval(carregarDadosMercado, 5000);
window.onload = carregarDadosMercado;