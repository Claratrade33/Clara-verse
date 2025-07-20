function abrirConfiguracoes() {
    document.getElementById("modal-config").style.display = "block";
}

function fecharConfiguracoes() {
    document.getElementById("modal-config").style.display = "none";
}

function salvarChaves() {
    const binanceKey = document.getElementById("binance_api_key").value;
    const binanceSecret = document.getElementById("binance_api_secret").value;
    const openaiKey = document.getElementById("openai_api_key").value;

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
    .then(response => response.json())
    .then(data => {
        alert("Chaves salvas com sucesso!");
        fecharConfiguracoes();

        // Atualiza o gráfico (reload do iframe)
        const graficoContainer = document.getElementById("grafico-container");
        graficoContainer.innerHTML = `
            <iframe src="https://www.binance.com/pt/trade/BTC_USDT?layout=basic"
                    width="100%" height="600px" frameborder="0"></iframe>
        `;
    })
    .catch(error => {
        alert("Erro ao salvar chaves.");
        console.error(error);
    });
}

function mostrarGrafico() {
    const graficoContainer = document.getElementById("grafico-container");
    graficoContainer.scrollIntoView({ behavior: "smooth" });
}