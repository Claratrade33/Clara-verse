from flask import Flask, render_template, request, redirect, session, jsonify
import requests
import os
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Login padrão
USUARIO_PADRAO = "admin"
SENHA_PADRAO = "claraverse2025"

# Armazenamento das chaves
chaves_salvas = {
    "binance_api_key": "",
    "binance_api_secret": "",
    "openai_api_key": ""
}

# Modo automático
modo_demo = True
saldo_demo = 10000.0  # R$10.000 de saldo fictício
operacoes_realizadas = []

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
    return render_template("painel.html", chaves=chaves_salvas, demo=modo_demo, saldo=saldo_demo)

@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    data = request.json
    chaves_salvas["binance_api_key"] = data.get("binance_api_key", "")
    chaves_salvas["binance_api_secret"] = data.get("binance_api_secret", "")
    chaves_salvas["openai_api_key"] = data.get("openai_api_key", "")
    global modo_demo
    modo_demo = not (chaves_salvas["binance_api_key"] and chaves_salvas["binance_api_secret"])
    return jsonify({"status": "sucesso", "modo": "demo" if modo_demo else "real"})

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

@app.route("/operar", methods=["POST"])
def operar():
    data = request.json
    direcao = data.get("direcao")  # "compra" ou "venda"
    valor = float(data.get("valor", 0))

    global saldo_demo
    if modo_demo:
        if direcao == "compra" and saldo_demo >= valor:
            saldo_demo -= valor
            operacoes_realizadas.append({"tipo": "compra", "valor": valor, "horario": time.time()})
            return jsonify({"status": "compra registrada (demo)", "saldo_restante": saldo_demo})
        elif direcao == "venda":
            saldo_demo += valor
            operacoes_realizadas.append({"tipo": "venda", "valor": valor, "horario": time.time()})
            return jsonify({"status": "venda registrada (demo)", "saldo_restante": saldo_demo})
        else:
            return jsonify({"status": "saldo insuficiente"})
    else:
        # Aqui seria feita a operação real com Binance se implementado
        return jsonify({"status": "operação real não implementada ainda"})

# Para o Render
application = app
