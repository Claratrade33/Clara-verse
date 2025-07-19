import os
import time
import hmac
import hashlib
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

API_KEY = os.getenv("Bia")
SECRET_KEY = os.getenv("Bia1").encode()

historico = []
meta_usdt = 50  # valor inicial de meta
modo_ativo = True

HTML = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ClaraVerse | Operação Real</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            background-color: #000;
            color: #fff;
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        h1 {
            font-size: 28px;
        }
        input, button {
            padding: 12px;
            margin: 10px 0;
            font-size: 16px;
        }
        .azul { background-color: #007BFF; color: white; border: none; }
        .verde { background-color: #00FFC2; color: black; border: none; }
        .vermelho { background-color: red; color: white; border: none; }
        .grafico {
            margin: 20px 0;
            background-color: #111;
            padding: 10px;
            border-radius: 10px;
        }
        .ordem {
            background: #111;
            padding: 10px;
            margin: 10px 0;
            border-left: 4px solid #00FFC2;
        }
    </style>
</head>
<body>
    <h1>🧠 ClarinhaBubi em Ação</h1>
    <form method="POST" action="/salvar-meta">
        <input type="number" name="meta" placeholder="Meta diária em USDT" required>
        <button class="azul" type="submit">Salvar Meta</button>
    </form>

    <form method="POST" action="/executar">
        <button class="verde" type="submit">🚀 Executar Ordem</button>
    </form>

    <form method="POST" action="/stop">
        <button class="vermelho" type="submit">🛑 STOP</button>
    </form>

    <div class="grafico">
        <iframe src="https://s.tradingview.com/embed-widget/mini-symbol-overview/?symbol=BINANCE:BTCUSDT&locale=br" 
                width="100%" height="220" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
    </div>

    <h2>Histórico de Ordens</h2>
    {% for o in historico %}
        <div class="ordem">
            <strong>Moeda:</strong> BTCUSDT<br>
            <strong>Lucro:</strong> {{ o['lucro'] }}<br>
            <strong>ROI:</strong> {{ o['roi'] }}%
        </div>
    {% endfor %}
</body>
</html>
'''

def executar_ordem(valor_usdt=10):
    try:
        base_url = "https://api.binance.com"
        endpoint = "/api/v3/order"
        url = base_url + endpoint

        timestamp = int(time.time() * 1000)
        symbol = "BTCUSDT"
        side = "BUY"
        type_ = "MARKET"

        query = f"symbol={symbol}&side={side}&type={type_}&quoteOrderQty={valor_usdt}&timestamp={timestamp}"
        signature = hmac.new(SECRET_KEY, query.encode(), hashlib.sha256).hexdigest()

        headers = {
            "X-MBX-APIKEY": API_KEY
        }

        full_url = f"{url}?{query}&signature={signature}"
        response = requests.post(full_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            preco = float(data["fills"][0]["price"])
            qty = float(data["executedQty"])
            lucro = round(qty * preco * 0.01, 2)
            roi = round((lucro / (qty * preco)) * 100, 2)
            historico.append({"lucro": lucro, "roi": roi})
            return f"✅ Ordem executada: {qty} BTC a {preco} USDT"
        else:
            return f"❌ Erro: {response.text}"
    except Exception as e:
        return f"Erro inesperado: {str(e)}"

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML, historico=historico)

@app.route("/executar", methods=["POST"])
def acionar_ordem():
    if modo_ativo:
        executar_ordem(meta_usdt)
    return render_template_string(HTML, historico=historico)

@app.route("/stop", methods=["POST"])
def parar():
    global modo_ativo
    modo_ativo = False
    return "🛑 Modo automático parado com sucesso."

@app.route("/salvar-meta", methods=["POST"])
def salvar_meta():
    global meta_usdt
    meta_usdt = float(request.form["meta"])
    return render_template_string(HTML, historico=historico)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
