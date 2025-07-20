from flask import Flask, render_template, request, redirect, session, jsonify
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 🔐 Login padrão
USUARIO_PADRAO = "admin"
SENHA_PADRAO = "claraverse2025"

# 🔒 Armazenamento temporário das chaves de API (em memória)
chaves_salvas = {
    "binance_api_key": "",
    "binance_api_secret": "",
    "openai_api_key": ""
}

# 🌐 Redireciona para a página inicial do dashboard
@app.route("/")
def home():
    return redirect("/dashboard")

# 📄 Página inicial com visual institucional (antes do login)
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# 🔐 Login com verificação de usuário e senha padrão
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

# 🚪 Logout e limpeza da sessão
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/login")

# 📊 Painel principal após login
@app.route("/painel")
def painel():
    if "usuario" not in session:
        return redirect("/login")
    return render_template("painel.html", chaves=chaves_salvas)

# 💾 Rota para salvar as chaves de API do usuário
@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    data = request.json
    chaves_salvas["binance_api_key"] = data.get("binance_api_key", "")
    chaves_salvas["binance_api_secret"] = data.get("binance_api_secret", "")
    chaves_salvas["openai_api_key"] = data.get("openai_api_key", "")
    return jsonify({"status": "sucesso"})

# 📈 Consulta de dados do mercado (via API pública da Binance)
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

# 🔁 Compatibilidade com Gunicorn no Render
application = app