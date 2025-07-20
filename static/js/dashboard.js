document.addEventListener("DOMContentLoaded", function () {
  const status = document.getElementById("status");
  const preco = document.getElementById("preco");
  const variacao = document.getElementById("variacao");
  const volume = document.getElementById("volume");

  // Atualiza o status de execução
  function atualizarStatus(texto) {
    status.textContent = texto;
  }

  // Simula execução de ordem (exemplo para demonstração)
  function simularOrdem(tipo) {
    atualizarStatus(`Enviando ordem de ${tipo}...`);
    setTimeout(() => {
      atualizarStatus(`✅ Ordem de ${tipo} executada com sucesso!`);
      preco.textContent = "117.979,20";
      variacao.textContent = "+0.12%";
      volume.textContent = "20 BTC";
    }, 2000);
  }

  // Detecta clique nos botões e executa ações
  const botoes = document.querySelectorAll(".sidebar ul li a");
  botoes.forEach(botao => {
    botao.addEventListener("click", function (e) {
      e.preventDefault();
      const texto = this.textContent.trim();

      switch (texto) {
        case "Entrada":
          simularOrdem("ENTRADA");
          break;
        case "Stop":
          simularOrdem("STOP");
          break;
        case "Alvo":
          simularOrdem("ALVO");
          break;
        case "Automático":
          simularOrdem("MODO AUTOMÁTICO");
          break;
        case "Configurar":
          atualizarStatus("Abrindo painel de configuração...");
          break;
        case "Sair":
          window.location.href = "/logout";
          break;
        default:
          atualizarStatus("⚠️ Comando não reconhecido.");
      }
    });
  });
});