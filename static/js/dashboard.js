async function executarAcao(acao) {
    try {
        const resposta = await fetch('/executar_acao', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ acao })
        });
        const resultado = await resposta.json();
        atualizarSaldo(resultado.saldo);
        mostrarMensagem(resultado.mensagem);
    } catch (erro) {
        console.error('Erro ao executar ação:', erro);
    }
}

async function obterSugestaoIA() {
    try {
        const resposta = await fetch('/obter_sugestao_ia');
        const resultado = await resposta.json();
        mostrarMensagem(resultado.resposta);
    } catch (erro) {
        console.error('Erro ao obter sugestão da IA:', erro);
        mostrarMensagem("❌ Erro ao consultar a IA.");
    }
}

async function atualizarSaldo(saldo) {
    const divSaldo = document.querySelector('.saldo');
    if (divSaldo) {
        divSaldo.innerText = `Saldo Atual: $${saldo.toFixed(2)} USDT`;
    }
}

function mostrarMensagem(msg) {
    const respostaIA = document.getElementById('resposta-ia');
    respostaIA.innerText = msg;
}