import time
import hmac
import hashlib
import requests
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)
app.secret_key = 'CLARAVERSE_2025'

# 🔐 Chaves reais blindadas e internas
API_KEY = 'Ule5h0cEFcLV8uXnhYZcF0nEUUu0nRANo9m6JLqupr8Xy3HKzh7aQHT6vW72YrVA'
API_SECRET = 'JDdOeKeo93NB8kdtqgcDL1pQhYGPMRJMcOFeHDISqYzQsCJqKfMSkVmy3G8gik36'

BASE_URL = "https://api.binance.com"
PAR_MOEDA = "BTCUSDT"
historico_operacoes = []

# 🌐 HTML completo com gráfico, botões e ROI
PAINEL = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ClaraVerse | Sala de Operações</title>
    <style>
        body { background: #000; color: #0ff; font-family: monospace; padding: 20px; text-align: center; }
        h1 { margin-top: 10px; }
        button { padding: 10px 20px; font-weight: bold; margin: 10px; cursor: pointer; border: none; }
        .executar { background: #00ffc8; color: #000; }
        .stop { background: #ff0044; color: #fff; }
        .bloco { background: #111; border-left: 4px solid #0ff; padding: 15px; margin: 20px auto; width: 80%; text-align: left; }
        iframe { border: none; margin-top: 30px; width: 100%; height: 400px; }
    </style>
</head>
<body>
    <h1>🚀 ClaraVerse | IA ClarinhaBubi Ativa</h1>
    
    <form method="POST" action="/executar">
        <button class="executar">💼 EXECUTAR ORDEM</button>
    </form>
    <form method="POST" action="/stop">
        <button class="stop">🛑 STOP</button>
    </form>

    <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark&style=1&locale=br" allowtransparency="true"></iframe>

    <h2>📊 ROI & HISTÓRICO</h2>
    {% for item in historico %}
        <div class="bloco">{{ item }}</div>
    {% endfor %}
</body>
</html>
"""

def obter_preco(par="BTCUSDT"):
    try:
        url = f"{BASE_URL}/api/v3/ticker/price"
        r = requests.get(url, params={"symbol": par})
        return float(r.json()['price'])
    except:
        return None

def enviar_ordem(par, lado, quantidade):
    timestamp = int(time.time() * 1000)
    query = f"symbol={par}&side={lado}&type=MARKET&quantity={quantidade}&timestamp={timestamp}"
    assinatura = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    url = f"{BASE_URL}/api/v3/order?{query}&signature={assinatura}"
    headers = {"X-MBX-APIKEY": API_KEY}
    resposta = requests.post(url, headers=headers)
    return resposta.json()

@app.route("/")
def painel():
    return render_template_string(PAINEL, historico=historico_operacoes)

@app.route("/executar", methods=["POST"])
def executar_ordem():
    try:
        preco_entrada = obter_preco(PAR_MOEDA)
        if preco_entrada:
            quantidade = round(15 / preco_entrada, 6)
            enviar_ordem(PAR_MOEDA, "BUY", quantidade)
            time.sleep(2)
            preco_saida = obter_preco(PAR_MOEDA)
            lucro = round((preco_saida - preco_entrada) * quantidade, 2)
            resultado = f"✅ Executado: {quantidade} BTC | Entrada: {preco_entrada} | Saída: {preco_saida} | ROI: {lucro} USDT"
            historico_operacoes.insert(0, resultado)
        else:
            historico_operacoes.insert(0, "⚠️ Erro ao obter preço.")
    except Exception as e:
        historico_operacoes.insert(0, f"❌ Erro: {e}")
    return redirect("/")

@app.route("/stop", methods=["POST"])
def parar():
    historico_operacoes.insert(0, "🛑 Operação interrompida manualmente.")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)