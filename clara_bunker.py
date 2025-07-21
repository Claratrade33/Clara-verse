from flask import Flask, render_template, request, redirect, session, jsonify
from cryptography.fernet import Fernet
import os, requests, openai

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Chave fixa para manter a criptografia viva entre deploys
CHAVE_CRIPTO_FIXA = b'xApbCQFxxa3Yy3YKkzP9JkkfE4WaXxN8eSpK7uBRuGA='
fernet = Fernet(CHAVE_CRIPTO_FIXA)

# Dados simulados
USUARIO_PADRAO = "admin"
SENHA_PADRAO = "claraverse2025"
saldo_simulado = 5000.0
chaves_criptografadas = {
    "binance_api_key": None,
    "binance_api_secret": None,
    "openai_api_key": None
}

# ===== ROTAS =====

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
    return render_template("painel.html", saldo=saldo_simulado)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/configurar")
def configurar():
    if "usuario" not in session:
        return redirect("/login")
    def descriptografar(valor):
        return fernet.decrypt(valor).decode() if valor else ""
    return render_template("configurar.html", chaves={
        "binance_api_key": descriptografar(chaves_criptografadas["binance_api_key"]),
        "binance_api_secret": descriptografar(chaves_criptografadas["binance_api_secret"]),
        "openai_api_key": descriptografar(chaves_criptografadas["openai_api_key"])
    })

@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    try:
        data = request.get_json()
        chaves_criptografadas["binance_api_key"] = fernet.encrypt(data.get("binance_api_key", "").encode())
        chaves_criptografadas["binance_api_secret"] = fernet.encrypt(data.get("binance_api_secret", "").encode())
        chaves_criptografadas["openai_api_key"] = fernet.encrypt(data.get("openai_api_key", "").encode())
        return jsonify({"status": "sucesso"})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)})

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

        chave_openai = fernet.decrypt(chaves_criptografadas["openai_api_key"]).decode() if chaves_criptografadas["openai_api_key"] else ""
        if not chave_openai:
            raise Exception("Chave OpenAI ausente.")

        openai.api_key = chave_openai
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": f"O preço atual do BTC é {preco}, com variação de {variacao}%. RSI em {rsi}. Qual a melhor sugestão para operação agora?"
            }]
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
    except Exception:
        return jsonify({
            "preco": "--", "variacao": "--", "volume": "--",
            "rsi": "--", "suporte": "--", "resistencia": "--",
            "sugestao": "Aguardando IA ou API incompleta."
        })

@app.route("/executar/<acao>", methods=["POST"])
def executar_acao(acao):
    global saldo_simulado
    respostas = {
        "entrada": "✅ Entrada realizada com base na análise!",
        "stop": "🛑 Stop acionado! Proteção ativada.",
        "alvo": "🎯 Alvo atingido! Lucro contabilizado.",
        "automatico": "🤖 Modo automático ativado. Clarinha assume!",
        "executar": "🚀 Ordem executada com sucesso!"
    }
    if acao == "entrada":
        saldo_simulado -= 50
    elif acao == "alvo":
        saldo_simulado += 100
    elif acao == "stop":
        saldo_simulado -= 30
    return jsonify({"mensagem": respostas.get(acao, "Ação desconhecida.")})

# Ponto de entrada do Render
application = app