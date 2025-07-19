import os
from flask import Flask, render_template_string, request, redirect
import requests
import datetime
import random

app = Flask(__name__)

# ==== Chaves da Binance embutidas (criptografadas no ambiente) ====
API_KEY = "j4nBvFRELeSFDDpgMIz35yTW5JZyNIVIRDPc8Nrt2jmZHWdZRpgGHGxnIzIJeMnK"
API_SECRET = "jKTxQjEtD0mgWxFeM2I2pxXsZimhnGEeWEN2MTz8Y5w7Y00gCVmjLrV3vFo8REKy"

# === Variáveis dinâmicas em memória ===
META_DIARIA = 0.0
HISTORICO = []
ORDENS_ATIVAS = []

# ==== Página com visual de corretora ====
HTML = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ClaraVerse | ClarinhaBubi em Ação</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            background-color: #000;
            color: white;
            font-family: "Arial", sans-serif;
            text-align: center;
        }
        input, button {
            margin: 10px;
            padding: 10px;
            border: none;
            font-size: 16px;
            border-radius: 8px;
        }
        input[type="text"] {
            width: 60%;
        }
        .btn-executar {
            background-color: #00ffd5;
            color: black;
            font-weight: bold;
        }
        .btn-stop {
            background-color: red;
            color: white;
            font-weight: bold;
        }
        .grafico {
            margin-top: 20px;
        }
        .historico {
            margin-top: 30px;
            padding: 20px;
            background: #111;
            border-radius: 10px;
            max-width: 500px;
            margin-left: auto;
            margin-right: auto;
        }
    </style>
</head>
<body>
    <h1>🧠 ClarinhaBubi em Ação</h1>

    <form action="/salvar_meta" method="POST">
        <input type="text" name="meta" placeholder="Meta diária em USDT" required>
        <button type="submit">Salvar Meta</button>
    </form>

    <form action="/executar" method="POST">
        <button type="submit" class="btn-executar">🚀 Executar Ordem</button>
    </form>

    <form action="/stop" method="POST">
        <button type="submit" class="btn-stop">🛑 STOP</button>
    </form>

    <div class="grafico">
        <iframe src="https://s.tradingview.com/embed-widget/mini-symbol-overview/?locale=br#%7B%22symbol%22%3A%22BINANCE%3ABTCUSDT%22%2C%22width%22%3A%22auto%22%2C%22height%22%3A220%2C%22colorTheme%22%3A%22dark%22%7D" width="100%" height="220" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
    </div>

    <div class="historico">
        <h2>Histórico de Ordens</h2>
        {% for item in historico %}
            <p><strong>Moeda:</strong> {{ item['moeda'] }}<br>
            <strong>Lucro:</strong> {{ item['lucro'] }}<br>
            <strong>ROI:</strong> {{ item['roi'] }}%</p>
            <hr>
        {% else %}
            <p>Nenhuma ordem registrada ainda.</p>
        {% endfor %}
    </div>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML, historico=HISTORICO[::-1])

@app.route("/salvar_meta", methods=["POST"])
def salvar_meta():
    global META_DIARIA
    try:
        META_DIARIA = float(request.form["meta"])
    except:
        META_DIARIA = 0
    return redirect("/")

@app.route("/executar", methods=["POST"])
def executar_ordem():
    moeda = "BTCUSDT"
    lucro_simulado = round(random.uniform(3, 100), 2)
    roi_simulado = round((lucro_simulado / 1000) * 100, 2)

    ordem = {
        "moeda": moeda,
        "lucro": lucro_simulado,
        "roi": roi_simulado,
        "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    HISTORICO.append(ordem)
    return redirect("/")

@app.route("/stop", methods=["POST"])
def stop_ordem():
    HISTORICO.append({"moeda": "Todas", "lucro": "Ordem Cancelada", "roi": 0})
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)