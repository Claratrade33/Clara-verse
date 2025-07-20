document.addEventListener("DOMContentLoaded", function () {
    // Botões principais
    const btnCall = document.querySelector('.btn-call');
    const btnPut = document.querySelector('.btn-put');

    // Elementos de status
    const statusTexto = document.getElementById('painel-status');
    const saldoTexto = document.getElementById('painel-saldo');

    // Simulação de saldo
    let saldo = 10000;
    let lucro = 0;

    function atualizarStatus(texto, cor = '#ffa726') {
        statusTexto.textContent = texto;
        statusTexto.style.color = cor;
    }

    function atualizarSaldo(valor) {
        saldo += valor;
        saldoTexto.textContent = `$${saldo.toFixed(2)}`;
    }

    function simularOrdem(direcao) {
        const resultado = Math.random();
        const ganho = resultado > 0.5 ? 87 : -100;
        const valorOrdem = 100;

        if (ganho > 0) {
            atualizarStatus(`✅ Ordem CALL bem-sucedida: +$${(valorOrdem * 0.87).toFixed(2)}`, '#00ff94');
            atualizarSaldo(valorOrdem * 0.87);
        } else {
            atualizarStatus(`❌ Ordem PUT falhou: -$${valorOrdem}`, '#ff5e57');
            atualizarSaldo(-valorOrdem);
        }
    }

    btnCall.addEventListener('click', function () {
        simularOrdem('call');
    });

    btnPut.addEventListener('click', function () {
        simularOrdem('put');
    });
});