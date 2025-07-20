from flask import Flask, render_template, request, redirect, session, jsonify
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 🔐 Login padrão
USUARIO_PADRAO = "admin"
SENHA_PADRAO = "claraverse2025"

# 🔒 Armazenamento temporário das chaves
chaves_salvas = {
    "binance_api_key": "",
    "binance_api_secret": "",
    "openai_api_key": ""
}

# 💰 Modo Demo
demo_saldo = {"BRL": 10000.00}

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        if usuario == USUARIO_PADRAO and senha == SENHA_PADRAO:
            session["usuario"] = usuario
            return redirect("/painel")
        else:
            return render_template("login.html", erro="Usuário ou senha incorretos.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/login")

@app.route("/painel")
def painel():
    if "usuario" not in session:
        return redirect("/login")
    return render_template("painel.html", saldo=demo_saldo["BRL"])

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

@app.route("/executar_ordem", methods=["POST"])
def executar_ordem():
    if "usuario" not in session:
        return jsonify({"status": "erro", "mensagem": "Usuário não autenticado"})
    
    dados = request.json
    direcao = dados.get("direcao")  # "call" ou "put"
    valor = float(dados.get("valor", 0))

    if valor > demo_saldo["BRL"]:
        return jsonify({"status": "erro", "mensagem": "Saldo insuficiente"})

    demo_saldo["BRL"] -= valor
    return jsonify({
        "status": "sucesso",
        "mensagem": f"Ordem {direcao.upper()} de R${valor:.2f} executada no modo demo!",
        "saldo_restante": f"R${demo_saldo['BRL']:.2f}"
    })

# 🔁 Para o Render
application = app