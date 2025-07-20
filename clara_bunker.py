from flask import Flask, render_template, request, redirect, session, jsonify
import os, requests, openai

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Login padrão
USUARIO_PADRAO = "admin"
SENHA_PADRAO = "claraverse2025"

# Armazenamento de chaves (temporário)
chaves_salvas = {
    "binance_api_key": "",
    "binance_api_secret": "",
    "openai_api_key": ""
}

# Redirecionamento raiz
@app.route("/")
def home():
    return redirect("/dashboard")

# Dashboard inicial
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Tela de login
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

# Logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/login")

# Painel principal
@app.route("/painel")
def painel():
    if "usuario" not in session:
        return redirect("/login")
    return render_template("painel.html", chaves=chaves_salvas)

# Página de configurações
@app.route("/configurar")
def configurar():
    if "usuario" not in session:
        return redirect("/login")
    return render_template("configurar.html", chaves=chaves_salvas)

# Salvar chaves da API
@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    data = request.json
    chaves_salvas["binance_api_key"] = data.get("binance_api_key", "")
    chaves_salvas["binance_api_secret"] = data.get("binance_api_secret", "")
    chaves_salvas["openai_api_key"] = data.get("openai_api_key", "")
    return jsonify({"status": "sucesso"})

# Dados do mercado (BTCUSDT)
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
            "preco": "--", "variacao": "--", "volume": "--"
        })

# Comando para IA tomar decisão (modo Iansã)
@app.route("/comando/<acao>")
def comando_ia(acao):
    openai.api_key = chaves_salvas["openai_api_key"]
    prompt = f"""
    Você é uma IA avançada de operações financeiras chamada ClaraVerse.
    Estratégia: {acao.upper()} para o par BTC/USDT.
    Responda com JSON contendo entrada, alvo, stop e nível de confiança.
    """
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        conteudo = resposta.choices[0].message.content
        return jsonify({"resposta": conteudo})
    except Exception as e:
        return jsonify({"erro": str(e)})

# Render compatível
application = app