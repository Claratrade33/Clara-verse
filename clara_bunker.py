from flask import Flask, render_template, request, redirect, session, jsonify
import os, requests, openai
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Geração/armazenamento de chave criptográfica (fixa em memória)
fernet_key = Fernet.generate_key()
fernet = Fernet(fernet_key)

# Dados persistentes simulados
USUARIO_PADRAO = "admin"
SENHA_PADRAO = "claraverse2025"
saldo_simulado = 5000

# Armazenamento criptografado em memória
chaves_criptografadas = {
    "binance_api_key": "",
    "binance_api_secret": "",
    "openai_api_key": ""
}

def criptografar(valor):
    return fernet.encrypt(valor.encode()).decode()

def descriptografar(valor):
    return fernet.decrypt(valor.encode()).decode()

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

    chaves = {
        "binance_api_key": descriptografar(chaves_criptografadas["binance_api_key"]) if chaves_criptografadas["binance_api_key"] else "",
        "binance_api_secret": descriptografar(chaves_criptografadas["binance_api_secret"]) if chaves_criptografadas["binance_api_secret"] else "",
        "openai_api_key": descriptografar(chaves_criptografadas["openai_api_key"]) if chaves_criptografadas["openai_api_key"] else ""
    }

    return render_template("painel.html", saldo=saldo_simulado, chaves=chaves)

@app.route("/configurar")
def configurar():
    if "usuario" not in session:
        return redirect("/login")

    chaves = {
        "binance_api_key": descriptografar(chaves_criptografadas["binance_api_key"]) if chaves_criptografadas["binance_api_key"] else "",
        "binance_api_secret": descriptografar(chaves_criptografadas["binance_api_secret"]) if chaves_criptografadas["binance_api_secret"] else "",
        "openai_api_key": descriptografar(chaves_criptografadas["openai_api_key"]) if chaves_criptografadas["openai_api_key"] else ""
    }

    return render_template("configurar.html", chaves=chaves)

@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    data = request.json
    if "usuario" not in session:
        return jsonify({"status": "erro", "mensagem": "Não autenticado."})

    chaves_criptografadas["binance_api_key"] = criptografar(data.get("binance_api_key", ""))
    chaves_criptografadas["binance_api_secret"] = criptografar(data.get("binance_api_secret", ""))
    chaves_criptografadas["openai_api_key"] = criptografar(data.get("openai_api_key", ""))

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

        openai.api_key = descriptografar(chaves_criptografadas["openai_api_key"]) if chaves_criptografadas["openai_api_key"] else ""
        prompt = f"O preço do BTC é {preco}, com variação de {variacao}%. RSI: {rsi}. Suporte: {suporte}, Resistência: {resistencia}. Qual a melhor decisão agora?"
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        sugestao = resposta["choices"][0]["message"]["content"]

        return jsonify({
            "preco": preco,
            "variacao": variacao,
            "volume": volume,
            "rsi": rsi,
            "suporte": suporte,
            "resistencia": resistencia,
            "sugestao": sugestao
        })
    except Exception as e:
        return jsonify({
            "preco": "--", "variacao": "--", "volume": "--",
            "rsi": "--", "suporte": "--", "resistencia": "--",
            "sugestao": "Erro ao consultar IA ou API pública."
        })

@app.route("/executar/<acao>", methods=["POST"])
def executar_acao(acao):
    global saldo_simulado
    respostas = {
        "entrada": "✅ ENTRADA: posição aberta com sucesso.",
        "stop": "🛑 STOP: proteção acionada.",
        "alvo": "🎯 ALVO: meta atingida.",
        "executar": "🚀 EXECUTAR: operação confirmada.",
        "automatico": "🤖 MODO AUTOMÁTICO ativado."
    }

    if acao == "entrada":
        saldo_simulado -= 100
    elif acao == "alvo":
        saldo_simulado += 150
    elif acao == "stop":
        saldo_simulado -= 80

    return jsonify({"mensagem": respostas.get(acao, "Ação desconhecida.")})

# Para Render
application = app