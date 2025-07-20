document.addEventListener("DOMContentLoaded", function () {
    const configForm = document.getElementById("config-form");

    if (configForm) {
        configForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const openaiKey = document.getElementById("openai-key").value;
            const binanceKey = document.getElementById("binance-key").value;
            const binanceSecret = document.getElementById("binance-secret").value;

            fetch("/salvar_chaves", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    openai_key: openaiKey,
                    binance_key: binanceKey,
                    binance_secret: binanceSecret,
                }),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message || "Chaves salvas com sucesso!");
            })
            .catch(error => {
                console.error("Erro ao salvar as chaves:", error);
                alert("Erro ao salvar as chaves.");
            });
        });
    }

    const analiseForm = document.getElementById("analise-form");
    if (analiseForm) {
        analiseForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const mensagem = document.getElementById("mensagem").value;
            const resultado = document.getElementById("resultado");

            fetch("/analise", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ mensagem }),
            })
            .then((res) => res.json())
            .then((data) => {
                resultado.innerHTML = `
                    <p><strong>Entrada:</strong> ${data.entrada}</p>
                    <p><strong>Alvo:</strong> ${data.alvo}</p>
                    <p><strong>Stop:</strong> ${data.stop}</p>
                    <p><strong>Confiança:</strong> ${data.confianca}</p>
                `;
            })
            .catch((err) => {
                resultado.innerHTML = "<p>Erro na análise. Verifique as chaves de API e tente novamente.</p>";
                console.error(err);
            });
        });
    }
});