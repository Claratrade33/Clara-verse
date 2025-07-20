from flask import Flask, render_template, request, redirect, session, jsonify
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 🔐 Login padrão
USUARIO_PADRAO = "admin"
SENHA_PADRAO = "claraverse2025"

# 🔒 Armazenamento simulado das chaves
chaves_salvas = {
    "binance_api_key": "",
    "binance_api_secret": "",
    "openai_api_key": ""
}

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    if usuario == USUARIO_PADRAO and senha == SENHA_PADRAO:
        session["usuario"] = usuario
        return redirect("/painel")
    return render_template("login.html", erro="Usuário ou senha incorretos.")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/painel")
def painel():
    if "usuario" not in session:
        return redirect("/")
    return render_template("painel.html")

@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    data = request.json
    chaves_salvas["binance_api_key"] = data.get("binance_api_key", "")
    chaves_salvas["binance_api_secret"] = data.get("binance_api_secret", "")
    chaves_salvas["openai_api_key"] = data.get("openai_api_key", "")
    return jsonify({"status": "sucesso"})

@app.route("/dados_mercado")
def dados_mercado():
    par = request.args.get("par", "BTCUSDT")
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={par}"
        response = requests.get(url)
        dados = response.json()
        return jsonify({
            "preco": dados.get("lastPrice", "--"),
            "variacao": dados.get("priceChangePercent", "--"),
            "volume": dados.get("volume", "--")
        })
    except:
        return jsonify({
            "preco": "--",
            "variacao": "--",
            "volume": "--"
        })

# 🔁 Para compatibilidade com Render
application = app