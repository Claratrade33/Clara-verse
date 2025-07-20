document.addEventListener("DOMContentLoaded", () => {
    atualizarDados();

    setInterval(atualizarDados, 15000); // atualiza mercado a cada 15s

    document.getElementById("btnEntrada").addEventListener("click", () => enviarComando("entrada"));
    document.getElementById("btnStop").addEventListener("click", () => enviarComando("stop"));
    document.getElementById("btnAlvo").addEventListener("click", () => enviarComando("alvo"));
    document.getElementById("btnAuto").addEventListener("click", () => enviarSugestao());
    document.getElementById("btnConfigurar").addEventListener("click", () => {
        window.location.href = "/configurar";
    });
});

function atualizarDados() {
    fetch("/dados_mercado")
        .then(res => res.json())
        .then(data => {
            document.getElementById("preco").textContent = data.preco;
            document.getElementById("variacao").textContent = data.variacao;
            document.getElementById("volume").textContent = data.volume;
        });
}

function enviarComando(comando) {
    alert(`Comando enviado: ${comando} (modo demo)`);
}

function salvarChaves() {
    const payload = {
        binance_api_key: document.getElementById("binance_api_key").value,
        binance_api_secret: document.getElementById("binance_api_secret").value,
        openai_api_key: document.getElementById("openai_api_key").value,
        meta_lucro: parseFloat(document.getElementById("meta_lucro").value || "2.5")
    };

    fetch("/salvar_chaves", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("status-chaves").textContent = "Chaves salvas com sucesso!";
        setTimeout(() => {
            document.getElementById("status-chaves").textContent = "";
        }, 3000);
    });
}

function enviarSugestao() {
    fetch("/api/sugestao")
        .then(res => res.json())
        .then(data => {
            const secao = document.createElement("div");
            secao.className = "sugestao-ia";
            secao.innerHTML = `
                <h3>✨ Sugestão da Clarinha</h3>
                <p>${data.resposta}</p>
                <button onclick="confirmarExecucao()">✅ Confirmar e Executar</button>
            `;
            document.querySelector(".painel-conteudo").appendChild(secao);
        });
}

function confirmarExecucao() {
    alert("✅ Ordem confirmada e enviada (modo demo)!");
}