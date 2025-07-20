document.addEventListener("DOMContentLoaded", function () {
    const status = document.getElementById("status");

    function ativarBotao(endpoint, botao) {
        status.textContent = "Executando...";
        status.classList.add("executando");
        status.classList.remove("sucesso", "erro");

        fetch(`/${endpoint}`, {
            method: "POST"
        })
        .then(response => response.json())
        .then(data => {
            status.textContent = data.status || "Concluído";
            status.classList.remove("executando");
            status.classList.add("sucesso");
        })
        .catch(error => {
            console.error("Erro:", error);
            status.textContent = "Erro na solicitação";
            status.classList.remove("executando");
            status.classList.add("erro");
        });
    }

    document.getElementById("entrada").addEventListener("click", function () {
        ativarBotao("entrada", this);
    });

    document.getElementById("stop").addEventListener("click", function () {
        ativarBotao("stop", this);
    });

    document.getElementById("alvo").addEventListener("click", function () {
        ativarBotao("alvo", this);
    });

    document.getElementById("automatico").addEventListener("click", function () {
        ativarBotao("automatico", this);
    });

    // Configuração (abre painel)
    document.getElementById("config").addEventListener("click", function () {
        window.location.href = "/config";
    });

    // Logout
    document.getElementById("logout").addEventListener("click", function () {
        window.location.href = "/logout";
    });
});