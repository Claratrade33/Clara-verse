from flask import Flask, render_template, request, jsonify
from cryptography.fernet import Fernet
import os
import json

app = Flask(__name__)
application = app

FERNET_KEY = os.environ.get("FERNET_KEY", Fernet.generate_key().decode())
fernet = Fernet(FERNET_KEY.encode() if isinstance(FERNET_KEY, str) else FERNET_KEY)

CHAVES_FILE = "chaves_config.json"

def salvar_chaves_seguras(api_key, api_secret, openai_key):
    chaves_criptografadas = {
        "binance_api_key": fernet.encrypt(api_key.encode()).decode(),
        "binance_api_secret": fernet.encrypt(api_secret.encode()).decode(),
        "openai_api_key": fernet.encrypt(openai_key.encode()).decode()
    }
    with open(CHAVES_FILE, "w") as f:
        json.dump(chaves_criptografadas, f)

def carregar_chaves():
    if not os.path.exists(CHAVES_FILE):
        return None
    with open(CHAVES_FILE, "r") as f:
        data = json.load(f)
    return {
        "binance_api_key": fernet.decrypt(data["binance_api_key"].encode()).decode(),
        "binance_api_secret": fernet.decrypt(data["binance_api_secret"].encode()).decode(),
        "openai_api_key": fernet.decrypt(data["openai_api_key"].encode()).decode()
    }

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/painel")
def painel():
    return render_template("painel.html")

@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    data = request.get_json()
    try:
        salvar_chaves_seguras(
            data["binance_api_key"],
            data["binance_api_secret"],
            data["openai_api_key"]
        )
        return jsonify({"success": True, "message": "Chaves salvas com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/carregar_chaves", methods=["GET"])
def get_chaves():
    try:
        chaves = carregar_chaves()
        if chaves:
            return jsonify({"success": True, "chaves": chaves})
        else:
            return jsonify({"success": False, "message": "Nenhuma chave salva."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})