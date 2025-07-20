document.addEventListener("DOMContentLoaded", () => {
    atualizarPreco();

    document.getElementById("btnAuto")?.addEventListener("click", enviarSugestao);
});

function atualizarPreco() {
    fetch("/dados_mercado")
        .then(res => res.json())
        .then(data => {
            document.getElementById("preco").textContent = data.preco || "--";
            document.getElementById("variacao").textContent = data.variacao || "--";
            document.getElementById("volume").textContent = data.volume || "--";
        })
        .catch(error => console.error("Erro ao buscar dados de mercado:", error));
}

function salvarChaves() {
    const binanceApiKey = document.getElementById("binance_api_key").value;
    const binanceApiSecret = document.getElementById("binance_api_secret").value;
    const openaiApiKey = document.getElementById("openai_api_key").value;
    const metaLucro = document.getElementById("meta_lucro")?.value || "";

    fetch("/salvar_chaves", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            binance_api_key: binanceApiKey,
            binance_api_secret: binanceApiSecret,
            openai_api_key: openaiApiKey,
            meta_lucro: metaLucro
        }),
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("status-chaves").textContent = data.mensagem;
    })
    .catch(error => console.error("Erro ao salvar chaves:", error));
}

function enviarComando(comando) {
    fetch("/executar_comando", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ comando: comando }),
    })
    .then(res => res.json())
    .then(data => alert(data.mensagem))
    .catch(error => console.error("Erro ao executar comando:", error));
}

// 🌟 Modo Automático – Pede sugestão à Clarinha (GPT)
function enviarSugestao() {
    fetch("/sugestao_ia")
        .then(res => res.json())
        .then(data => {
            const painel = document.createElement("div");
            painel.className = "painel-sugestao";
            painel.innerHTML = `
                <h3>✨ Sugestão da Clarinha</h3>
                <p><strong>Entrada:</strong> ${data.entrada}</p>
                <p><strong>Alvo:</strong> ${data.alvo}</p>
                <p><strong>Stop:</strong> ${data.stop}</p>
                <p><strong>Confiança:</strong> ${data.confianca}</p>
                <button onclick='confirmarExecucao(${JSON.stringify(data)})'>Confirmar e Executar</button>
            `;

            const container = document.querySelector(".painel-conteudo");
            const anterior = document.querySelector(".painel-sugestao");
            if (anterior) anterior.remove(); // Remove anterior se houver
            container.appendChild(painel);
        })
        .catch(error => console.error("Erro ao obter sugestão da IA:", error));
}

// ✅ Confirmar execução da sugestão da IA
function confirmarExecucao(dados) {
    fetch("/executar_sugestao", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
    })
    .then(res => res.json())
    .then(data => alert(data.mensagem))
    .catch(error => console.error("Erro ao confirmar execução:", error));
}