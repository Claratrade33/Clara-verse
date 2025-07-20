from flask import Flask, render_template, request, redirect, session, jsonify
import requests, os, openai, json
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = os.urandom(24)

USUARIO_PADRAO = "admin"
SENHA_PADRAO = "claraverse2025"

# Caminho do arquivo criptografado
CAMINHO_CHAVES = "chaves_segredas.bin"

# Geração e uso da chave de criptografia
if not os.path.exists("segredo.key"):
    with open("segredo.key", "wb") as f:
        f.write(Fernet.generate_key())

with open("segredo.key", "rb") as f:
    chave_fernet = Fernet(f.read())

def salvar_chaves_criptografadas(dados):
    criptografado = chave_fernet.encrypt(json.dumps(dados).encode())
    with open(CAMINHO_CHAVES, "wb") as f:
        f.write(criptografado)

def carregar_chaves_criptografadas():
    if not os.path.exists(CAMINHO_CHAVES):
        return {"binance_api_key": "", "binance_api_secret": "", "openai_api_key": ""}
    try:
        with open(CAMINHO_CHAVES, "rb") as f:
            dados = chave_fernet.decrypt(f.read()).decode()
            return json.loads(dados)
    except:
        return {"binance_api_key": "", "binance_api_secret": "", "openai_api_key": ""}

@app.route("/")
def home():
    return redirect("/painel")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("usuario") == USUARIO_PADRAO and request.form.get("senha") == SENHA_PADRAO:
            session["usuario"] = USUARIO_PADRAO
            return redirect("/painel")
        return render_template("login.html", erro="Login inválido.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/login")

@app.route("/painel")
def painel():
    if "usuario" not in session:
        return redirect("/login")
    chaves = carregar_chaves_criptografadas()
    return render_template("painel.html", chaves=chaves, saldo="5000.00")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/configurar")
def configurar():
    if "usuario" not in session:
        return redirect("/login")
    chaves = carregar_chaves_criptografadas()
    return render_template("configurar.html", chaves=chaves)

@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    data = request.json
    salvar_chaves_criptografadas({
        "binance_api_key": data.get("binance_api_key", ""),
        "binance_api_secret": data.get("binance_api_secret", ""),
        "openai_api_key": data.get("openai_api_key", "")
    })
    return jsonify({"status": "sucesso"})

@app.route("/dados_mercado")
def dados_mercado():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
        r = requests.get(url).json()
        preco = r.get("lastPrice", "--")
        variacao = r.get("priceChangePercent", "--")
        volume = r.get("quoteVolume", "--")

        rsi = round(50 + float(variacao)/2, 2)
        suporte = round(float(variacao) - 0.8, 2)
        resistencia = round(float(variacao) + 0.8, 2)

        chaves = carregar_chaves_criptografadas()
        openai.api_key = chaves["openai_api_key"]
        prompt = f"O preço do BTC é {preco} com variação {variacao}%. RSI em {rsi}. Suporte {suporte}, resistência {resistencia}. Qual a melhor decisão agora?"
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        sugestao = resposta["choices"][0]["message"]["content"]

        return jsonify({
            "preco": preco, "variacao": variacao, "volume": volume,
            "rsi": rsi, "suporte": suporte, "resistencia": resistencia,
            "sugestao": sugestao
        })

    except Exception as e:
        return jsonify({
            "preco": "--", "variacao": "--", "volume": "--",
            "rsi": "--", "suporte": "--", "resistencia": "--",
            "sugestao": "Erro ao carregar dados."
        })

@app.route("/executar/<acao>", methods=["POST"])
def executar_acao(acao):
    acoes = {
        "entrada": "✅ ENTRADA feita com sucesso!",
        "stop": "🛑 STOP ativado!",
        "alvo": "🎯 ALVO alcançado!",
        "automatico": "🤖 Modo automático ativado.",
        "executar": "🚀 Execução em andamento conforme IA."
    }
    return jsonify({"mensagem": acoes.get(acao, "Ação desconhecida.")})

# Render compatibilidade
application = app