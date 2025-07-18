# clara_bunker.py
import os
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from binance.client import Client
from cryptography.fernet import Fernet
import openai

# ========= SEGURANÇA E CONFIGURAÇÕES =========
fernet_key = b'0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA='
fernet = Fernet(fernet_key)

# Chaves protegidas (padrão demo)
api_key_demo = fernet.decrypt(b'gAAAAABmzyEYzvXKsvhRDLi_BiZP3hP_pP8qWFe0NT2MT5x8NNXsk4MrwY1rErjgbG3P-fPVmjQBP3KpH7OJIF7eMI4dPH6c5w==').decode()
api_secret_demo = fernet.decrypt(b'gAAAAABmzyEZF2AD88qnlL61GJt0Ml2J3WvE2XNpMwYQHrlu0YG0sG3EGFJYxYIlpEQhUVTJQ0Ht_wH0is6TYy6ScenogbCEGA==').decode()

# OPENAI Key (protegida)
openai.api_key = fernet.decrypt(b'gAAAAABmzyEZCOKaIu0IVRA6l0FMhwY9u4UlTLF8Br4FJzjVub3HqDLVG-8vMNo1AsbyYzQ44D0P3bRfMROFT9Z7ffptRht4Dg==').decode()

# ========= FLASK APP =========
app = Flask(__name__)
app.secret_key = 'ClaraVerseBunkerUltraSecreto'

# ========= DEMO CLIENT =========
client = Client(api_key_demo, api_secret_demo, testnet=True)

# ========= ROTAS =========

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        token = request.form["token"].strip().upper()
        session["token"] = token
        return redirect("/sala-operacoes")
    return """
    <form method='post'>
        <input name='token' placeholder='Digite seu token'>
        <button type='submit'>Entrar</button>
    </form>
    """

@app.route("/sala-operacoes")
def sala():
    token = session.get("token", "")
    if token not in ["SOMA", "INFINITY", "DESPERTAR", "VEUS", "ORIGEM", "ANJOS"]:
        return "🔒 Acesso negado."
    return """
    <h1>💎 Sala de Operações ClaraVerse</h1>
    <p>Modo atual: Demo</p>
    <form method="post" action="/executar">
        <button type="submit">🚀 Executar Ordem</button>
    </form>
    <form method="post" action="/ativar-automatico">
        <button type="submit">🤖 Ativar Modo Automático</button>
    </form>
    """

@app.route("/executar", methods=["POST"])
def executar_ordem():
    ordem = client.create_test_order(
        symbol='BTCUSDT',
        side='BUY',
        type='MARKET',
        quantity=0.001
    )
    return "✅ Ordem executada com sucesso! (modo demo)"

@app.route("/ativar-automatico", methods=["POST"])
def ativar_auto():
    token = session.get("token", "")
    if token not in ["SOMA", "INFINITY", "DESPERTAR"]:
        return "⚠️ Token não tem permissão para IA automática."
    
    # Simulação de decisão da IA
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é a IA ClarinhaBubi, uma estrategista de ordens da Binance."},
            {"role": "user", "content": "Qual decisão devo tomar agora no mercado BTCUSDT em modo demo com 10.000 USDT?"}
        ]
    )
    analise = resposta["choices"][0]["message"]["content"]
    return f"<pre>{analise}</pre>"

# ========= INÍCIO =========
if __name__ == "__main__":
    app.run(debug=True)
application = app