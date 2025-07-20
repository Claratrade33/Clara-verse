// Atualiza os dados do mercado a cada 5 segundos
function atualizarDadosMercado() {
    fetch('/dados_mercado?par=BTCUSDT')
        .then(res => res.json())
        .then(data => {
            document.getElementById("preco").textContent = data.preco;
            document.getElementById("variacao").textContent = data.variacao;
            document.getElementById("volume").textContent = data.volume;
        })
        .catch(() => {
            document.getElementById("preco").textContent = "--";
            document.getElementById("variacao").textContent = "--";
            document.getElementById("volume").textContent = "--";
        });
}
setInterval(atualizarDadosMercado, 5000);
window.onload = atualizarDadosMercado;

// Salvar as chaves via /salvar_chaves
function salvarChaves() {
    const dados = {
        binance_api_key: document.getElementById("binance_api_key").value,
        binance_api_secret: document.getElementById("binance_api_secret").value,
        openai_api_key: document.getElementById("openai_api_key").value
    };

    fetch("/salvar_chaves", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(dados)
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("status-chaves").textContent = "🔒 Chaves salvas com sucesso!";
        document.getElementById("status-chaves").style.color = "lime";
    })
    .catch(() => {
        document.getElementById("status-chaves").textContent = "Erro ao salvar as chaves.";
        document.getElementById("status-chaves").style.color = "red";
    });
}

// Envia o tipo de comando para futura lógica (entrada, stop, alvo, automático)
function enviarComando(tipo) {
    alert(`⚙️ Comando '${tipo.toUpperCase()}' ativado! (em modo de demonstração)`);

    // Aqui você poderá futuramente conectar com /executar_acao ou outra rota com lógica real.
}