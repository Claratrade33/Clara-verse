from flask import Flask, render_template_string, request, jsonify
import time, threading, random
from binance.client import Client
from cryptography.fernet import Fernet

# === CHAVE DE CRIPTOGRAFIA (fixa, segura e blindada) ===
fernet = Fernet(b"iLOW9XW_YzPQ8ePWhpHFcESuLORJ25JUNAWgW1cFv9s=")
API_KEY_CRYPT = "gAAAAABoewAoQ-KQgJ1cuR2biUn66fBCu96z_T3_POD41svHnGJ2lSE70Ftd7Mxm6Y8CLObvcFSqb26dxEi3szCSuAeZ252IjnS316FjXM68NUpGBnx10nA="
API_SECRET_CRYPT = "gAAAAABoewAo0gQUy-XtwAgjfEPXBVAkhRlt7eNJeBRe1pe5J4Uv2FsWnPi-boLINgfg2s4345Fe9OMfy8Ip5FicEi07rqP8Kc9fPzv4N9EhgMejXTPPQDo="

API_KEY = fernet.decrypt(API_KEY_CRYPT.encode()).decode()
API_SECRET = fernet.decrypt(API_SECRET_CRYPT.encode()).decode()

client = Client(API_KEY, API_SECRET)

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>ClaraVerse Bunker 🚨</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { background: black; color: white; font-family: monospace; text-align: center; padding: 30px; }
    iframe { width: 90%; max-width: 800px; height: 400px; border: 4px solid #00ffcc; border-radius: 10px; margin-bottom: 20px; }
    button { margin: 10px; padding: 14px 24px; font-size: 18px; font-weight: bold; border: none; border-radius: 8px;
             background-color: #00ffcc; color: #000; cursor: pointer; box-shadow: 0 0 20px #00ffcc88; }
    .msg { margin-top: 20px; padding: 20px; background: #111; border-left: 5px solid #00ffcc; border-radius: 8px; }
  </style>
</head>
<body>
  <h1>🚨 Clarinha Operando no Modo Real 🚨</h1>
  <iframe src="https://www.tradingview.com/embed-widget/mini-symbol-overview/?symbol=BINANCE:BTCUSDT&locale=br"></iframe>
  <br>
  <button onclick="operar()">Operar Manual</button>
  <button onclick="auto()">Modo Automático</button>
  <div id="saida" class="msg">🧠 Aguardando comandos...</div>
  <script>
    function operar() {
      fetch('/manual', { method: 'POST' })
        .then(res => res.json())
        .then(data => { document.getElementById('saida').innerText = data.resultado; });
    }
    function auto() {
      fetch('/auto', { method: 'POST' })
        .then(res => res.json())
        .then(data => { document.getElementById('saida').innerText = data.resultado; });
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(html)

@app.route("/manual", methods=["POST"])
def manual():
    try:
        symbol = "BTCUSDT"
        price = float(client.get_symbol_ticker(symbol=symbol)["price"])
        quantity = round(8 / price, 6)
        order = client.create_test_order(symbol=symbol, side="BUY", type="MARKET", quantity=quantity)
        return jsonify({"resultado": f"✔️ Ordem manual preparada: {quantity} {symbol}"})
    except Exception as e:
        return jsonify({"resultado": f"❌ Erro: {str(e)}"})

@app.route("/auto", methods=["POST"])
def auto():
    def estrategia():
        for _ in range(10):
            try:
                price = float(client.get_symbol_ticker(symbol="BTCUSDT")["price"])
                q = round(8 / price, 6)
                client.create_test_order(symbol="BTCUSDT", side="BUY", type="MARKET", quantity=q)
                print(f"🧠 Clarinha executou uma ordem: {q} BTC")
                time.sleep(random.uniform(1, 3))
            except:
                continue
    threading.Thread(target=estrategia).start()
    return jsonify({"resultado": "🛠️ Clarinha ativada no modo automático!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)