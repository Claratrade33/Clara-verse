from flask import Flask, render_template_string, request, jsonify
import hmac, hashlib, time, base64, requests
from cryptography.fernet import Fernet

app = Flask(__name__)

fernet_key = "0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="
fernet = Fernet(fernet_key.encode())

def decrypt_key(encrypted):
    return fernet.decrypt(encrypted.encode()).decode()

API_KEY_CRYPT = "gAAAAABoe5Gx09W-9VRMzfWFvcsfnAkAbQxYwdqvHC_oX9bFSnvSyJWxdQO3d5xZdGCdWCjmv48IKHlF1ZA1bSIMPzqvh2-TKw=="
API_SECRET_CRYPT = "gAAAAABoe5GxNIwgEqJkp1OJxW9Jsi-Qy53LTG98lQ8HCbVheYkTYgUUIYXmslo-7Dp9QHW0Q5lu5dqSoIK2gq_2-Yw_tylrUg=="

API_KEY = decrypt_key(API_KEY_CRYPT)
API_SECRET = decrypt_key(API_SECRET_CRYPT)

@app.route("/")
def home():
    return render_template_string("""
    <html>
    <head><title>ClaraVerse Corretora Inteligente</title></head>
    <body>
        <h1>Bem-vindo à ClaraVerse</h1>
        <form method="POST" action="/executar">
            <input name="symbol" placeholder="Símbolo (ex: BTCUSDT)">
            <input name="side" placeholder="buy/sell">
            <input name="qty" placeholder="Quantidade">
            <button type="submit">Executar Ordem</button>
        </form>
    </body>
    </html>
    """)

@app.route("/executar", methods=["POST"])
def executar_ordem():
    symbol = request.form.get("symbol")
    side = request.form.get("side")
    quantity = request.form.get("qty")

    endpoint = "https://fapi.binance.com/fapi/v1/order"
    timestamp = int(time.time() * 1000)
    params = f"symbol={symbol}&side={side.upper()}&type=MARKET&quantity={quantity}&timestamp={timestamp}"
    signature = hmac.new(API_SECRET.encode(), params.encode(), hashlib.sha256).hexdigest()
    url = f"{endpoint}?{params}&signature={signature}"
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    response = requests.post(url, headers=headers)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
