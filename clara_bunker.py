from flask import Flask, render_template_string, request
from binance.client import Client
import time

# 🔒 Chaves protegidas (reais)
API_KEY = "j4nBvFRELeSFDDpgMIz35yTW5JZyNIVIRDPC8Nrt2jmZHWDzRpgGHGxnIzIJeMnK"
API_SECRET = "jkTxQjEtD0mgWxFeM2I2pxXsZimhnGEeWEN2MTz8Y5w7Y00gCVmjLrV3vFo8REKy"

client = Client(API_KEY, API_SECRET)

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ClaraVerse | Sala de Operações</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            background-color: #000;
            color: #0ff;
            font-family: monospace;
            text-align: center;
            padding: 30px;
        }
        .botao {
            background-color: #00ffff;
            border: none;
            color: #000;
            padding: 15px 30px;
            margin: 10px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
        }
        .painel {
            margin-top: 40px;
            border: 2px solid #0ff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 12px #00ffff66;
        }
        .log {
            background-color: #111;
            color: #0f0;
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
            display: inline-block;
            min-width: 300px;
        }
    </style>
</head>
<body>
    <h1>🧠 ClarinhaBubi<br>na Sala de Operações</h1>
    <form method="POST" action="/executar">
        <button class="botao" type="submit">EXECUTAR ORDEM</button>
    </form>
    <form method="POST" action="/automatica">
        <button class="botao" type="submit">MODO AUTOMÁTICO</button>
    </form>
    <div class="painel">
        <h3>📄 Ordens Executadas:</h3>
        {% if mensagem %}
        <div class="log">{{ mensagem }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/executar", methods=["POST"])
def executar():
    try:
        ordem = client.order_market_buy(
            symbol="BTCUSDT",
            quantity=0.00015  # valor baixo pra segurança
        )
        mensagem = f"✅ Ordem executada: {ordem['symbol']} - ID: {ordem['orderId']}"
    except Exception as e:
        mensagem = f"❌ Erro: {str(e)}"
    return render_template_string(HTML, mensagem=mensagem)

@app.route("/automatica", methods=["POST"])
def automatica():
    try:
        profundidade = client.get_order_book(symbol="BTCUSDT")
        lance = float(profundidade['bids'][0][0])
        ask = float(profundidade['asks'][0][0])
        direcao = "buy" if lance < ask else "sell"
        quantidade = 0.00015

        if direcao == "buy":
            ordem = client.order_market_buy(symbol="BTCUSDT", quantity=quantidade)
        else:
            ordem = client.order_market_sell(symbol="BTCUSDT", quantity=quantidade)

        mensagem = f"🤖 Ordem {direcao} automática executada com sucesso! ID: {ordem['orderId']}"
    except Exception as e:
        mensagem = f"❌ Erro Automático: {str(e)}"
    return render_template_string(HTML, mensagem=mensagem)

if __name__ == "__main__":
    app.run(debug=True)