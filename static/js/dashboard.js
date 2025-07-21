// Atualizar saldo
function atualizarSaldo() {
    fetch('/obter_saldo')
        .then(response => response.json())
        .then(data => {
            document.querySelector('.saldo').textContent = `Saldo Atual: $${data.saldo} USDT`;
        });
}

// Atualizar preço BTC
function atualizarPrecoBTC() {
    fetch('/obter_preco')
        .then(response => response.json())
        .then(data => {
            document.getElementById('preco-btc').textContent = `BTC/USDT: $${data.preco}`;
        });
}

// Executar ações
function executarAcao(acao) {
    fetch('/executar_acao', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ acao })
    })
    .then(response => response.json())
    .then(data => {
        atualizarSaldo();
        mostrarMensagem(data.mensagem);
    });
}

// Sugestão da IA
function obterSugestaoIA() {
    fetch('/obter_sugestao_ia')
        .then(response => response.json())
        .then(data => {
            document.getElementById('resposta-ia').textContent = data.resposta;
        });
}

// Mostrar mensagem
function mostrarMensagem(texto) {
    const box = document.getElementById('resposta-ia');
    box.textContent = texto;
}

// Gráfico em tempo real com Chart.js
let grafico;

function iniciarGrafico() {
    const ctx = document.getElementById('grafico-btc').getContext('2d');
    grafico = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'BTC/USDT',
                data: [],
                borderColor: '#00ffff',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            scales: {
                x: { display: false },
                y: { beginAtZero: false }
            }
        }
    });
}

function atualizarGrafico() {
    fetch('/obter_preco')
        .then(response => response.json())
        .then(data => {
            const agora = new Date().toLocaleTimeString();
            grafico.data.labels.push(agora);
            grafico.data.datasets[0].data.push(data.preco);
            if (grafico.data.labels.length > 20) {
                grafico.data.labels.shift();
                grafico.data.datasets[0].data.shift();
            }
            grafico.update();
        });
}

// Inicialização
window.onload = () => {
    atualizarSaldo();
    atualizarPrecoBTC();
    iniciarGrafico();
    setInterval(atualizarSaldo, 10000);
    setInterval(atualizarPrecoBTC, 5000);
    setInterval(atualizarGrafico, 5000);
};