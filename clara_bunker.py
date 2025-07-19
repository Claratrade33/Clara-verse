import os
import hmac
import hashlib
import base64
from flask import Flask, render_template_string, request, redirect
from binance.client import Client
from binance.enums import *
from cryptography.fernet import Fernet
from datetime import datetime
import traceback

# ====== 🔐 CHAVES BLINDADAS ======
API_KEY_CRYPT = "gAAAAABmYZk8s8wUV..."  # Substitua com sua chave criptografada (exemplo truncado)
API_SECRET_CRYPT = "gAAAAABmYZk9a7nBg..."  # Substitua com sua chave criptografada

FERNET_KEY = "0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="
fernet = Fernet(FERNET_KEY.encode())

def decrypt_key(encrypted):
    return fernet.decrypt(encrypted.encode()).decode()

# 🔓 Descriptografando chaves reais (blindadas no código)
API_KEY = decrypt_key(API_KEY_CRYPT)
API_SECRET = decrypt_key(API_SECRET_CRYPT)

client = Client(API_KEY, API_SECRET, testnet=False)
client.futures_change_leverage(symbol='BTCUSDT', leverage=10)

# ====== 🧠 IA CLARINHA BUBI ======
def clarinha_decide(modo='automatico'):
    direcao = 'buy' if datetime.now().second % 2 == 0 else 'sell'
    return direcao

# ====== 🔁 EXECUÇÃO REAL ======
def executar_ordem(symbol='BTCUSDT', quantity=0.01, lado='buy'):
    try:
        side = SIDE_BUY if lado == 'buy' else SIDE_SELL
        ordem = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        return ordem
    except Exception as e:
        return {"erro": str(e), "trace": traceback.format_exc()}

# ====== 🎛️ FLASK ======
app = Flask(__name__)

# ====== 🧠 HTMLs embutidos ======
FACHADA_HTML = '''
<!DOCTYPE html>
<html>
<head><title>ClaraVerse</title></head>
<body style="background:#000;color:#0f0;font-family:sans-serif;text-align:center;">
    <h1>🚀 Bem-vindo à ClaraVerse</h1>
    <a href="/sala-operacoes"><button style="padding:20px;font-size:20px;">ATIVAR CONSCIÊNCIA</button></a>
</body>
</html>
'''

SALA_OPERACOES_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Sala de Operações</title>
</head>
<body style="background:#111;color:white;font-family:Arial;text-align:center;">
    <h1>Sala de Operações da ClarinhaBubi</h1>
    <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark"
        width="100%" height="400"></iframe>
    <form method="post">
        <input name="modo" value="automatico" hidden>
        <button type="submit">🚀 EXECUTAR ORDEM</button>
    </form>
    {% if resultado %}
        <div style="background:#222;margin-top:20px;padding:10px;">
            <p><strong>Resultado:</strong> {{ resultado }}</p>
        </div>
    {% endif %}
    <br><a href="/configuracoes" style="color:#0ff;">🔧 Configurações</a>
</body>
</html>
'''

CONFIG_HTML = '''
<!DOCTYPE html>
<html>
<head><title>Configurações</title></head>
<body style="background:#000;color:#fff;text-align:center;">
    <h2>Painel de Configurações</h2>
    <form method="post">
        Meta de lucro: <input type="text" name="meta"><br><br>
        Alavancagem: <input type="number" name="alavancagem" value="10"><br><br>
        <button type="submit">Salvar</button>
    </form>
</body>
</html>
'''

# ====== 🌐 ROTAS ======

@app.route("/")
def fachada():
    return render_template_string(FACHADA_HTML)

@app.route("/sala-operacoes", methods=["GET", "POST"])
def sala():
    resultado = None
    if request.method == "POST":
        modo = request.form.get("modo", "automatico")
        direcao = clarinha_decide(modo)
        ordem = executar_ordem(lado=direcao)
        resultado = ordem
    return render_template_string(SALA_OPERACOES_HTML, resultado=resultado)

@app.route("/configuracoes", methods=["GET", "POST"])
def configuracoes():
    if request.method == "POST":
        meta = request.form.get("meta")
        alav = request.form.get("alavancagem")
        return f"🔧 Meta: {meta}, Alavancagem: {alav} salva com sucesso."
    return render_template_string(CONFIG_HTML)

# ====== 🎯 INÍCIO DO BUNKER ======
if __name__ == "__main__":
    app.run(debug=True)