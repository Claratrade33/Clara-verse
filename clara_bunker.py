# clara_bunker.py
import os
import time
import hmac
import base64
import hashlib
import requests
from cryptography.fernet import Fernet
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Chave Fernet para criptografia (já protegida)
FERNET_KEY = "0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="
fernet = Fernet(FERNET_KEY)

# Chaves reais da Binance já criptografadas (exemplo fictício)
API_KEY_CRYPT = "gAAAAABm6Bx4yG-EXEMPLOkFZ5UqHLgl..."
API_SECRET_CRYPT = "gAAAAABm6Bx4z-EXEMPLO0D1HHdhflk3..."

# Descriptografar chaves
API_KEY = fernet.decrypt(API_KEY_CRYPT.encode()).decode()
API_SECRET = fernet.decrypt(API_SECRET_CRYPT.encode()).decode()

# Endpoint da Binance (testnet por padrão)
BASE_URL = "https://testnet.binancefuture.com"

# Cabeçalhos com chave
def get_headers(query_string):
    timestamp = int(time.time() * 1000)
    query_string += f"&timestamp={timestamp}"
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    query_string += f"&signature={signature}"
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    return headers, query_string

# Executar ordem pela Clarinha
def executar_ordem_clarinha(symbol="BTCUSDT", side="BUY", quantity=0.01):
    endpoint = "/fapi/v1/order"
    params = f"symbol={symbol}&side={side}&type=MARKET&quantity={quantity}"
    headers, final_query = get_headers(params)
    url = BASE_URL + endpoint + "?" + final_query
    response = requests.post(url, headers=headers)
    return response.json()

# HTML simples com botão de operação
html = '''
<!DOCTYPE html>
<html>
<head>
  <title>Clarinha na Binance</title>
</head>
<body style="background:#0f0f0f;color:#00ffcc;font-family:Arial;text-align:center;padding-top:50px">
  <h1>ClaraVerse: Clarinha operando 💎</h1>
  <form action="/executar" method="post">
    <button style="padding:20px 40px;font-size:20px;background:#00ffcc;border:none;border-radius:10px;color:#000;">EXECUTAR ORDEM</button>
  </form>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(html)

@app.route("/executar", methods=["POST"])
def executar():
    resultado = executar_ordem_clarinha()
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
