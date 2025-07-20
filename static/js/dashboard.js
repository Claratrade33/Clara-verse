document.addEventListener("DOMContentLoaded", function () {
    buscarDadosMercado();
    setInterval(buscarDadosMercado, 10000);
});

function buscarDadosMercado() {
    fetch("/dados_mercado")
        .then(res => res.json())
        .then(data => {
            document.getElementById("preco").textContent = data.preco;
            document.getElementById("variacao").textContent = data.variacao;
            document.getElementById("volume").textContent = data.volume;
        });
}

function salvarChaves() {
    const payload = {
        binance_api_key: document.getElementById("binance_api_key").value,
        binance_api_secret: document.getElementById("binance_api_secret").value,
        openai_api_key: document.getElementById("openai_api_key").value,
        meta_lucro: document.getElementById("meta_lucro") ? document.getElementById("meta_lucro").value : null
    };

    fetch("/salvar_chaves", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("status-chaves").textContent = "Configurações salvas com sucesso!";
    });
}

function enviarComando(tipo) {
    fetch(`/executar_comando?tipo=${tipo}`)
        .then(res => res.json())
        .then(data => {
            alert(`🧠 ClaraVerse:\n${data.mensagem}`);
        });
}