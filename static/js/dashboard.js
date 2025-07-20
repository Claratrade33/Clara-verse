// Atualização de preço ao vivo (Binance API pública)
async function atualizarDados() {
    try {
        const res = await fetch("/dados_mercado");
        const dados = await res.json();
        document.getElementById("preco").innerText = dados.preco;
        document.getElementById("variacao").innerText = dados.variacao + "%";
        document.getElementById("volume").innerText = dados.volume;
    } catch (e) {
        console.error("Erro ao obter dados de mercado:", e);
    }
}

// Botões de operação
function enviarComando(acao) {
    fetch("/operar", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ acao: acao })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.mensagem || "Comando enviado!");
    })
    .catch(() => {
        alert("Erro ao enviar comando.");
    });
}

// Configuração de API
function salvarChaves() {
    const binanceKey = document.getElementById("binanceKey").value;
    const binanceSecret = document.getElementById("binanceSecret").value;
    const openaiKey = document.getElementById("openaiKey").value;

    fetch("/salvar_chaves", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            binance_api_key: binanceKey,
            binance_api_secret: binanceSecret,
            openai_api_key: openaiKey
        })
    })
    .then(res => res.json())
    .then(data => {
        alert("Chaves salvas com sucesso!");
        fecharModal();
    });
}

// Modal
document.getElementById("btnConfig").addEventListener("click", () => {
    document.getElementById("modalConfig").style.display = "block";
});

function fecharModal() {
    document.getElementById("modalConfig").style.display = "none";
}

// Fechar modal clicando fora
window.onclick = function(event) {
    const modal = document.getElementById("modalConfig");
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

// Inicia
atualizarDados();
setInterval(atualizarDados, 10000); // Atualiza a cada 10s