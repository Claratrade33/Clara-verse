import hmac
import hashlib
import time
import requests
import json
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 🔐 Chaves reais fornecidas pela comandante protegida
API_KEY = 'Dja8iu8fmP34qAr8Tvh4VNsWo4GYbahCNxvDadvwfGCJTx3qP1JST9jBfteGPOdV'
SECRET_KEY = 'vwWP2lnNHNWKSMNCL7mLURIeJ29fCfjFOBZON9dvzLFMsp6XGjeLaDWsWKwfknc2'

BASE_URL = 'https://fapi.binance.com'

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ClarinhaBubi na Sala de Operações</title>
    <style>
        body { background-color: black; color: #00ffff; font-family: monospace; text-align: center; padding: 40px; }
        button { background-color: #00ffff; border: none; color: black; padding: 15px; font-size: 16px; margin: 10px; cursor: pointer; border-radius: 5px; }
        .log { background-color: #111; margin: 20px auto; padding: 15px; border-radius: 8px; max-width: 500px; box-shadow: 0 0 10px #00ffff88; }
    </style>
</head>
<body>
    <h1>🧠 ClarinhaBubi na Sala de Operações</h1>
    <form method="POST" action="/executar">
        <button type="submit">EXECUTAR ORDEM</button>
    </form>
    <form method="POST" action="/automatico">
        <button type="submit">MODO AUTOMÁTICO</button>
    </form>
    <h2>📄 Ordens Executadas:</h2>
    {% for log in logs %}
        <div class="log">{{ log }}</div>
    {% endfor %}
</body>
</html>
"""

logs = []

def assinar(params):
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    assinatura = hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return assinatura

def enviar_ordem():
    try:
        caminho = "/fapi/v1/order"
        timestamp = int(time.time() * 1000)

        params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "MARKET",
            "quantity": 0.001,
            "timestamp": timestamp
        }

        params["signature"] = assinar(params)

        headers = {
            "X-MBX-APIKEY": API_KEY
        }

        url = BASE_URL + caminho
        response = requests.post(url, headers=headers, params=params)

        if response.status_code == 200:
            resultado = response.json()
            logs.append(f"✅ Ordem executada: {json.dumps(resultado)}")
        else:
            logs.append(f"❌ Erro: {response.text}")
    except Exception as e:
        logs.append(f"❌ Exceção: {str(e)}")

@app.route('/', methods=["GET"])
def index():
    return render_template_string(HTML, logs=logs[-5:])

@app.route('/executar', methods=["POST"])
def executar():
    enviar_ordem()
    return render_template_string(HTML, logs=logs[-5:])

@app.route('/automatico', methods=["POST"])
def automatico():
    for _ in range(3):
        enviar_ordem()
        time.sleep(5)
    return render_template_string(HTML, logs=logs[-5:])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)