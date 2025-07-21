let chart;
let historico = [];

async function atualizarPreco() {
    try {
        const res = await fetch('/obter_preco');
        const data = await res.json();
        document.getElementById('preco').innerText = `$${parseFloat(data.preco).toFixed(2)}`;
        historico.push(parseFloat(data.preco));
        if (historico.length > 20) historico.shift();
        atualizarGrafico();
    } catch {
        document.getElementById('preco').innerText = 'Erro';
    }
}

async function atualizarSaldo() {
    try {
        const res = await fetch('/obter_saldo');
        const data = await res.json();
        const saldoElem = document.querySelector('.saldo');
        if (saldoElem) {
            saldoElem.innerText = `💰 Saldo Atual: $${data.saldo} USDT`;
        }
    } catch (e) {
        console.log('Erro saldo:', e);
    }
}

function atualizarGrafico() {
    if (!chart) return;
    chart.data.labels = historico.map((_, i) => i + 1);
    chart.data.datasets[0].data = historico;
    chart.update();
}

async function executarAcao(acao) {
    try {
        const res = await fetch('/executar_acao', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ acao })
        });
        const data = await res.json();
        alert(data.mensagem);
        atualizarSaldo();
    } catch (e) {
        alert('Erro ao executar ação');
    }
}

async function obterSugestaoIA() {
    try {
        const respostaElem = document.getElementById('respostaTexto');
        if (respostaElem) respostaElem.innerText = '⏳ Consultando Clarinha...';

        const res = await fetch('/obter_sugestao_ia', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: 'Sugira uma ação de trading para o par BTC/USDT.' })
        });

        const data = await res.json();
        if (respostaElem) respostaElem.innerText = data.resposta || '❌ Erro na resposta da IA';
    } catch (e) {
        const respostaElem = document.getElementById('respostaTexto');
        if (respostaElem) respostaElem.innerText = 'Erro ao consultar IA.';
    }
}

window.onload = () => {
    const graficoContainer = document.getElementById("grafico");
    if (graficoContainer) {
        const ctx = document.createElement("canvas");
        ctx.id = "graficoBTC";
        graficoContainer.appendChild(ctx);

        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Preço BTC/USDT',
                    data: [],
                    borderColor: 'cyan',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: false }
                }
            }
        });
    }

    atualizarPreco();
    atualizarSaldo();
    setInterval(() => {
        atualizarPreco();
        atualizarSaldo();
    }, 7000);
};