document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("modal-config");
  const btnAbrir = document.getElementById("btn-configuracoes");
  const btnFechar = document.getElementById("fechar-modal");
  const btnSalvar = document.getElementById("salvar-chaves");
  const statusConexao = document.getElementById("status-conexao");

  // Abre o modal
  btnAbrir.addEventListener("click", () => {
    modal.style.display = "block";
  });

  // Fecha o modal
  btnFechar.addEventListener("click", () => {
    modal.style.display = "none";
  });

  // Salva as chaves
  btnSalvar.addEventListener("click", () => {
    const binanceApiKey = document.getElementById("binance-api-key").value;
    const binanceApiSecret = document.getElementById("binance-api-secret").value;
    const openaiApiKey = document.getElementById("openai-api-key").value;

    fetch("/salvar_chaves", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        binance_api_key: binanceApiKey,
        binance_api_secret: binanceApiSecret,
        openai_api_key: openaiApiKey,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "sucesso") {
          modal.style.display = "none";
          statusConexao.innerText = "🔗 Conectado com sucesso!";
        }
      })
      .catch((err) => {
        console.error("Erro ao salvar as chaves:", err);
        statusConexao.innerText = "❌ Erro ao conectar.";
      });
  });

  // Botão automático envia comando para IA (em breve)
  document.getElementById("btn-auto").addEventListener("click", () => {
    alert("🧠 Modo automático com IA ainda em treinamento!");
  });
});