// dashboard.js

document.addEventListener("DOMContentLoaded", function() {
    // Função para obter o preço
    function obterPreco() {
        fetch('/obter_preco')
            .then(response => response.json())
            .then(data => {
                if (data.preco) {
                    document.getElementById("preco").innerText = `Preço BTC: $${data.preco}`;
                } else {
                    console.error(data.erro);
                }
            });
    }

    // Função para obter saldo
    function obterSaldo() {
        fetch('/obter_saldo')
            .then(response => response.json())
            .then(data => {
                if (data.saldo) {
                    document.getElementById("saldo").innerText = `Saldo USDT: $${data.saldo}`;
                } else {
                    console.error(data.erro);
                }
            });
    }

    // Função para executar ação
    function executarAcao(acao) {
        fetch('/executar_acao', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ acao: acao }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensagem) {
                alert(data.mensagem);
            } else {
                console.error(data.erro);
            }
        });
    }

    // Chame as funções para obter preço e saldo ao carregar o painel
    obterPreco();
    obterSaldo();

    // Adicione event listeners para botões, se necessário
    document.getElementById("comprarBtn").addEventListener("click", function() {
        executarAcao('comprar');
    });

    document.getElementById("venderBtn").addEventListener("click", function() {
        executarAcao('vender');
    });
});