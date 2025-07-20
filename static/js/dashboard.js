// Atualiza dados do mercado em tempo real
async function atualizarDadosMercado() {
    try {
        const response = await fetch('/dados_mercado');
        const data = await response.json();
        document.getElementById("preco").innerText = data.preco;
        document.getElementById("variacao").innerText = data.variacao;
        document.getElementById("volume").innerText = data.volume;
    } catch (e) {
        console.error("Erro ao buscar dados do mercado:", e);
    }
}

// Atualiza a cada 10 segundos
setInterval(atualizarDadosMercado, 10000);
document.addEventListener("DOMContentLoaded", atualizarDadosMercado);

// Salva as chaves de API com segurança
async function salvarChaves() {
    const binance_api_key = document.getElementById("binance_api_key").value;
    const binance_api_secret = document.getElementById("binance_api_secret").value;
    const openai_api_key = document.getElementById("openai_api_key").value;

    const resposta = await fetch("/salvar_chaves", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            binance_api_key,
            binance_api_secret,
            openai_api_key
        })
    });

    const resultado = await resposta.json();
    if (resultado.status === "sucesso") {
        document.getElementById("status-chaves").innerText = "🔐 Chaves salvas com sucesso!";
        setTimeout(() => {
            document.getElementById("status-chaves").innerText = "";
        }, 3000);
    }
}

// Envia comandos como ENTRADA, STOP, ALVO, AUTOMÁTICO
async function enviarComando(tipo) {
    const resposta = await fetch(`/executar_comando?tipo=${tipo}`);
    const resultado = await resposta.json();

    if (resultado.status === "ok") {
        alert(`✅ Comando ${tipo.toUpperCase()} enviado com sucesso!\nIA respondeu: ${resultado.mensagem}`);
    } else {
        alert(`❌ Erro ao executar comando ${tipo.toUpperCase()}`);
    }
}