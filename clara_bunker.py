from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import json
from binance.client import Client
from openai import OpenAI
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "claraverse_secure_key"
app.permanent_session_lifetime = timedelta(days=7)

# === Funções de API (vazias até usuário configurar via painel) ===
user_configs = {
    "openai_key": "",
    "binance_key": "",
    "binance_secret": ""
}

# === Página Inicial ===
@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

# === Login e Cadastro Simples ===
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if username == "admin" and password == "claraverse2025":
        session["user"] = username
        return redirect(url_for("dashboard"))
    return "Login inválido"

# === Logout ===
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

# === Painel Principal ===
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("dashboard.html")

# === Salvar Chaves de API ===
@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    data = request.get_json()
    user_configs["openai_key"] = data.get("openai_key", "")
    user_configs["binance_key"] = data.get("binance_key", "")
    user_configs["binance_secret"] = data.get("binance_secret", "")
    return jsonify({"status": "ok", "mensagem": "Chaves salvas com sucesso!"})

# === Rota de Análise com OpenAI ===
@app.route("/analise", methods=["POST"])
def analise():
    if not user_configs["openai_key"]:
        return jsonify({"erro": "Chave da OpenAI não configurada."})

    try:
        prompt = request.json.get("mensagem", "")
        client = OpenAI(api_key=user_configs["openai_key"])
        resposta = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        conteudo = resposta.choices[0].message.content
        return jsonify({"resposta": conteudo})
    except Exception as e:
        return jsonify({"erro": str(e)})

# === Rota para Dados de Gráfico (usando API pública da Binance) ===
@app.route("/grafico")
def grafico():
    try:
        binance = Client()
        klines = binance.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1HOUR, limit=100)
        dados = [
            {"tempo": k[0], "abertura": float(k[1]), "maxima": float(k[2]), "minima": float(k[3]), "fechamento": float(k[4])}
            for k in klines
        ]
        return jsonify(dados)
    except Exception as e:
        return jsonify({"erro": str(e)})

if __name__ == "__main__":
    app.run(debug=True)