let chart;
let historico = [];

async function atualizarPreco() {
    try {
        const res = await fetch('/obter_preco');
        const data = await res.json();

        if (data.preco) {
            document.getElementById('preco').innerText = `$${parseFloat(data.preco).toFixed(2)}`;
            historico.push(parseFloat(data.preco));

            if (historico.length > 20) {
                historico.shift(); // Remove o primeiro elemento se o histórico exceder 20
            }
            atualizarGrafico();
        } else {
            throw new Error('Preço não disponível');
        }
    } catch (error) {
        console.error('Erro ao obter preço:', error);
        document.getElementById('preco').innerText = 'Erro ao obter preço';
    }
}

async function atualizarSaldo() {
    try {
        const res = await fetch('/obter_saldo');
        const data = await res.json();
        document.querySelector('.saldo').innerText = `💰 Saldo Atual: $${data.saldo} USDT`;
    } catch (error) {
        console.error('Erro ao obter saldo:', error);
        document.querySelector('.saldo').innerText = 'Erro ao obter saldo';
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
    } catch (error) {
        alert('Erro ao executar ação: ' + error.message);
    }
}

async function obterSugestaoIA() {
    try {
        document.getElementById('respostaTexto').innerText = '⏳ Consultando Clarinha...';
        const res = await fetch('/obter_sugestao_ia');
        const data = await res.json();

        if (data.resposta) {
            document.getElementById('respostaTexto').innerText = data.resposta;
        } else {
            throw new Error('Resposta da IA não disponível');
        }
    } catch (error) {
        document.getElementById('respostaTexto').innerText = 'Erro ao consultar IA: ' + error.message;
    }
}

window.onload = () => {
    const ctx = document.createElement("canvas");
    ctx.id = "graficoBTC";
    document.getElementById("grafico").appendChild(ctx);

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

    atualizarPreco();
    atualizarSaldo();
    setInterval(() => {
        atualizarPreco();
        atualizarSaldo();
    }, 7000);
};