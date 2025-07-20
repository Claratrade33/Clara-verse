document.addEventListener("DOMContentLoaded", function () {
  const salvarBtn = document.getElementById("salvarChaves");
  const testarBtn = document.getElementById("testarConexao");

  if (salvarBtn) {
    salvarBtn.addEventListener("click", async function () {
      const binanceApiKey = document.getElementById("binance_api_key").value.trim();
      const binanceApiSecret = document.getElementById("binance_api_secret").value.trim();
      const openaiApiKey = document.getElementById("openai_api_key").value.trim();

      if (!binanceApiKey || !binanceApiSecret || !openaiApiKey) {
        alert("Por favor, preencha todos os campos de chave API.");
        return;
      }

      const resposta = await fetch("/salvar_chaves", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ binance_api_key: binanceApiKey, binance_api_secret: binanceApiSecret, openai_api_key: openaiApiKey })
      });

      const resultado = await resposta.json();
      if (resultado.status === "sucesso") {
        alert("✅ Chaves salvas com sucesso!");
      } else {
        alert("⚠️ Erro ao salvar as chaves.");
      }
    });
  }

  if (testarBtn) {
    testarBtn.addEventListener("click", async function () {
      const binanceApiKey = document.getElementById("binance_api_key").value.trim();
      const binanceApiSecret = document.getElementById("binance_api_secret").value.trim();
      const openaiApiKey = document.getElementById("openai_api_key").value.trim();

      if (!binanceApiKey || !binanceApiSecret || !openaiApiKey) {
        alert("Preencha as chaves para testar a conexão.");
        return;
      }

      const resposta = await fetch("/testar_conexoes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ binance_api_key: binanceApiKey, binance_api_secret: binanceApiSecret, openai_api_key: openaiApiKey })
      });

      const resultado = await resposta.json();

      let mensagem = "";
      mensagem += resultado.binance === "ok" ? "✅ Binance: OK\n" : "❌ Binance: Falha\n";
      mensagem += resultado.openai === "ok" ? "✅ OpenAI: OK" : "❌ OpenAI: Falha";

      alert(mensagem);
    });
  }
});