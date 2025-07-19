import os
import time
import hmac
import hashlib
import requests
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)
app.secret_key = 'CLARAVERSE_BUNKER_2025'

# 🔒 Chaves reais blindadas e embutidas
API_KEY = 'Ule5h0cEFcLV8uXnhYZcF0nEUUu0nRANo9m6JLqupr8Xy3HKzh7aQHT6vW72YrVA'
API_SECRET = 'JDdOeKeo93NB8kdtqgcDL1pQhYGPMRJMcOFeHDISqYzQsCJqKfMSkVmy3G8gik36'

BINANCE_URL = "https://api.binance.com"
PAIR = "BTCUSDT"
HISTORICO = []

# HTML com gráfico e painel estilo corretora
PAINEL = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ClaraVerse - Sala de Operações</title>
    <style>
        body { background: #000; color: #0ff; font-family: monospace; text-align: center; padding: 30px; }
        button { background: #0ff; color: #000; border: none; padding: 10px 20px; font-weight: bold; margin: 10px; cursor: pointer; }
        .stop { background: #f00; color: #fff; }
        .bloco { background: #111; padding: 15px; margin: 20px auto; width: 80%; border-left: 4px solid #0ff; text-align: left; }
        iframe { border: none; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>🚀 ClaraVerse | IA Ativa</h1>
    <form method="POST" action="/executar"><button>💼 Executar Ordem</button></form>
    <form method="POST" action="/stop"><button class="stop">🛑 STOP</button></form>
    
    <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_xxx&symbol=BINANCE:BTCUSDT&interval=1&theme=dark&style=1&locale=br#%7B%7D" width="100%" height="400"></iframe>

    <h2>📊 Histórico de ROI</h2>
    {% for item in historico %}
        <div class="bloco">{{ item }}</div>
    {% endfor %}
</body>
</html>
"""

def get_price(symbol="BTCUSDT"):
    url = f"{BINANCE_URL}/api/v3/ticker/price"
    response = requests.get(url, params={"symbol": symbol})
    return float(response.json()["price"])

def place_order(symbol, side, quantity):
    timestamp = int(time.time() * 1000)
    query_string = f"symbol={symbol}&side={side}&type=MARKET&quantity={quantity}&timestamp={timestamp}"
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    url = f"{BINANCE_URL}/api/v3/order?{query_string}&signature={signature}"
    return requests.post(url, headers={"X-MBX-APIKEY": API_KEY})

@app.route("/", methods=["GET"])
def index():
    return render_template_string(PAINEL, historico=HISTORICO)

@app.route("/executar", methods=["POST"])
def executar():
    try:
        preco_entrada = get_price(PAIR)
        quantidade = round(15 / preco_entrada, 6)
        ordem = place_order(PAIR, "BUY", quantidade)
        time.sleep(2)
        preco_saida = get_price(PAIR)
        lucro = round((preco_saida - preco_entrada) * quantidade, 2)
        texto = f"✅ Compra {quantidade} {PAIR} | Entrada: {preco_entrada} | Saída: {preco_saida} | ROI: {lucro} USDT"
        HISTORICO.insert(0, texto)
    except Exception as e:
        HISTORICO.insert(0, f"⚠️ Erro na operação: {e}")
    return redirect("/")

@app.route("/stop", methods=["POST"])
def stop():
    HISTORICO.insert(0, "🛑 Operação interrompida manualmente.")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)