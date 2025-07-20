document.addEventListener("DOMContentLoaded", async function () {
    const precoEl = document.getElementById("preco");
    const variacaoEl = document.getElementById("variacao");
    const volumeEl = document.getElementById("volume");
    const rsiEl = document.getElementById("rsi");
    const suporteEl = document.getElementById("suporte");
    const resistenciaEl = document.getElementById("resistencia");
    const sugestaoEl = document.getElementById("sugestao-texto");

    async function atualizarInfo() {
        try {
            const resposta = await fetch("/dados_mercado");
            const dados = await resposta.json();

            precoEl.innerText = `Preço: $${dados.preco}`;
            variacaoEl.innerText = `Variação: ${dados.variacao}%`;
            volumeEl.innerText = `Volume: ${dados.volume}`;
            rsiEl.innerText = `RSI: ${dados.rsi}`;
            suporteEl.innerText = `SUP: ${dados.suporte}%`;
            resistenciaEl.innerText = `RÉS: ${dados.resistencia}%`;

            sugestaoEl.innerText = dados.sugestao || "Carregando sugestão da Clarinha...";

        } catch (erro) {
            console.error("Erro ao buscar dados do mercado:", erro);
        }
    }

    async function executarAcao(acao) {
        try {
            const resposta = await fetch(`/executar/${acao}`, { method: "POST" });
            const resultado = await resposta.json();
            alert(`✅ ${resultado.mensagem}`);
        } catch (erro) {
            alert("❌ Erro ao executar ação.");
            console.error(erro);
        }
    }

    document.getElementById("btn-entrada").addEventListener("click", () => executarAcao("entrada"));
    document.getElementById("btn-stop").addEventListener("click", () => executarAcao("stop"));
    document.getElementById("btn-alvo").addEventListener("click", () => executarAcao("alvo"));
    document.getElementById("btn-automatico").addEventListener("click", () => executarAcao("automatico"));
    document.getElementById("btn-executar").addEventListener("click", () => executarAcao("executar"));

    setInterval(atualizarInfo, 8000);
    atualizarInfo();
});