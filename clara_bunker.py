from flask import Flask, render_template, request, redirect, session, jsonify
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

USUARIO_PADRAO = "admin"
SENHA_PADRAO = "claraverse2025"

chaves_salvas = {
    "binance_api_key": "",
    "binance_api_secret": "",
    "openai_api_key": "",
    "meta_lucro": ""
}

@app.route("/")
def home():
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("usuario") == USUARIO_PADRAO and request.form.get("senha") == SENHA_PADRAO:
            session["usuario"] = USUARIO_PADRAO
            return redirect("/painel")
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
    return render_template("painel.html", chaves=chaves_salvas)

@app.route("/configurar")
def configurar():
    if "usuario" not in session:
        return redirect("/login")
    return render_template("configurar.html", chaves=chaves_salvas)

@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    data = request.json
    for key in chaves_salvas:
        chaves_salvas[key] = data.get(key, "")
    return jsonify({"status": "sucesso"})

@app.route("/dados_mercado")
def dados_mercado():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT")
        d = r.json()
        return jsonify({"preco": d.get("lastPrice", "--"), "variacao": d.get("priceChangePercent", "--"), "volume": d.get("volume", "--")})
    except:
        return jsonify({"preco": "--", "variacao": "--", "volume": "--"})

@app.route("/executar_comando")
def executar_comando():
    tipo = request.args.get("tipo")
    if tipo == "entrada":
        msg = "Entrada registrada com sucesso!"
    elif tipo == "stop":
        msg = "Stop acionado!"
    elif tipo == "alvo":
        msg = "Alvo definido!"
    elif tipo == "auto":
        msg = "Modo automático ativado com IA ClaraVerse."
    else:
        msg = "Comando desconhecido."
    return jsonify({"mensagem": msg})

application = app