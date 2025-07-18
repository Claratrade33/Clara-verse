import os
from binance.client import Client
from cryptography.fernet import Fernet
from flask import Flask, jsonify

app = Flask(__name__)

# =========================
# 🔐 Recupera e descriptografa chaves seguras do ambiente
# =========================
FERNET_KEY = os.getenv("FERNET_KEY")
API_KEY_CRYPT = os.getenv("API_KEY_CRYPT")
API_SECRET_CRYPT = os.getenv("API_SECRET_CRYPT")

if not FERNET_KEY or not API_KEY_CRYPT or not API_SECRET_CRYPT:
    raise Exception("Variáveis de ambiente faltando!")

fernet = Fernet(FERNET_KEY.encode())
API_KEY = fernet.decrypt(API_KEY_CRYPT.encode()).decode()
API_SECRET = fernet.decrypt(API_SECRET_CRYPT.encode()).decode()

# =========================
# 🤖 Cliente da Binance
# =========================
client = Client(API_KEY, API_SECRET)

@app.route("/")
def index():
    return jsonify({"mensagem": "🔒 ClaraBunker ON | Protegida e Conectada à Binance!"})

@app.route("/saldo")
def saldo():
    try:
        info = client.get_account()
        return jsonify(info)
    except Exception as e:
        return jsonify({"erro": str(e)})

if __name__ == "__main__":
    app.run(debug=True)