async function executarAcao(acao) {
    const resposta = await fetch('/executar_acao', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ acao })
    });

    const dados = await resposta.json();
    document.getElementById('resposta-ia').innerText = dados.mensagem;
    document.getElementById('saldo').innerText = `$${dados.saldo}`;
}

async function obterSugestaoIA() {
    document.getElementById('resposta-ia').innerText = 'Consultando Clarinha...';

    const resposta = await fetch('/obter_sugestao_ia');
    const dados = await resposta.json();
    document.getElementById('resposta-ia').innerText = dados.resposta;
}