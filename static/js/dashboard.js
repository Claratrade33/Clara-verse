document.addEventListener("DOMContentLoaded", () => {
    carregarDadosMercado();

    const botoes = {
        entrada: document.getElementById("btnEntrada"),
        stop: document.getElementById("btnStop"),
        alvo: document.getElementById("btnAlvo"),
        auto: document.getElementById("btnAuto"),
        configurar: document.getElementById("btnConfigurar")
    };

    Object.keys(botoes).forEach(key => {
        if (botoes[key]) {
            botoes[key].addEventListener("click", () => {
                enviarComando(key);
            });
        }
    });
});

function carregarDadosMercado() {
    fetch("/dados_mercado")
        .then(res => res.json())
        .then(dados => {
            document.getElementById("preco").textContent = dados.preco;
            document.getElementById("variacao").textContent = dados.variacao;
            document.getElementById("volume").textContent = dados.volume;
        });
}

function enviarComando(acao) {
    fetch(`/executar_comando?acao=${acao}`)
        .then(res => res.json())
        .then(dados => {
            const secaoAI = document.querySelector(".secao-ai pre");
            if (secaoAI) {
                secaoAI.textContent = dados.mensagem || "Comando enviado!";
            }
        });
}

function salvarChaves() {
    const payload = {
        binance_api_key: document.getElementById("binance_api_key").value,
        binance_api_secret: document.getElementById("binance_api_secret").value,
        openai_api_key: document.getElementById("openai_api_key").value
    };

    fetch("/salvar_chaves", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    }).then(res => res.json())
      .then(res => {
          document.getElementById("status-chaves").textContent = "Chaves salvas com sucesso!";
      });
}