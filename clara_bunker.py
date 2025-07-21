from flask import Flask, render_template, request, redirect, session, jsonify
from cryptography.fernet import Fernet
import requests, os, openai

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Geração e uso de chave de criptografia
chave_fernet = Fernet.generate_key()
cipher = Fernet(chave_fernet)

# Armazenamento seguro na memória
chaves_criptografadas = {
    "binance_api_key": b"",
    "binance_api_secret": b"",
    "openai_api_key": b""
}

USUARIO_PADRAO = "admin"
SENHA_PADRAO = "claraverse2025"

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
    saldo_simulado = 5000
    return render_template("painel.html", saldo=saldo_simulado)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/configurar")
def configurar():
    if "usuario" not in session:
        return redirect("/login")
    def dec(b): return cipher.decrypt(b).decode() if b else ""
    return render_template("configurar.html", chaves={
        "binance_api_key": dec(chaves_criptografadas["binance_api_key"]),
        "binance_api_secret": dec(chaves_criptografadas["binance_api_secret"]),
        "openai_api_key": dec(chaves_criptografadas["openai_api_key"]),
    })

@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    try:
        data = request.json
        chaves_criptografadas["binance_api_key"] = cipher.encrypt(data.get("binance_api_key", "").encode())
        chaves_criptografadas["binance_api_secret"] = cipher.encrypt(data.get("binance_api_secret", "").encode())
        chaves_criptografadas["openai_api_key"] = cipher.encrypt(data.get("openai_api_key", "").encode())
        return jsonify({"status": "sucesso", "redirect": "/painel"})
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

        openai.api_key = cipher.decrypt(chaves_criptografadas["openai_api_key"]).decode()
        prompt = f"O preço do BTC está em {preco}, variação de {variacao}%, RSI em {rsi}. Qual a melhor estratégia?"
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
    except:
        return jsonify({
            "preco": "--", "variacao": "--", "volume": "--",
            "rsi": "--", "suporte": "--", "resistencia": "--",
            "sugestao": "Erro ao carregar dados."
        })

@app.route("/executar/<acao>", methods=["POST"])
def executar_acao(acao):
    respostas = {
        "entrada": "✅ Entrada simulada com sucesso!",
        "stop": "🛑 Stop acionado.",
        "alvo": "🎯 Alvo atingido.",
        "executar": "🚀 Ordem executada pela IA.",
        "automatico": "🤖 Modo automático ativado."
    }
    return jsonify({"mensagem": respostas.get(acao, "Ação não reconhecida.")})

# Compatível com Render
application = app