from flask import Flask, render_template, request, redirect, session, jsonify
import os, requests, openai
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Caminhos dos arquivos
KEY_PATH = "chave_secreta.key"
DADOS_PATH = "dados_criptografados.bin"

# Criar chave criptográfica se não existir
if not os.path.exists(KEY_PATH):
    with open(KEY_PATH, "wb") as f:
        f.write(Fernet.generate_key())

with open(KEY_PATH, "rb") as f:
    fernet = Fernet(f.read())

# Funções de criptografia
def salvar_dados(dados):
    criptografado = fernet.encrypt(str(dados).encode())
    with open(DADOS_PATH, "wb") as f:
        f.write(criptografado)

def carregar_dados():
    if not os.path.exists(DADOS_PATH):
        return {"binance_api_key": "", "binance_api_secret": "", "openai_api_key": ""}
    with open(DADOS_PATH, "rb") as f:
        return eval(fernet.decrypt(f.read()).decode())

# Dados iniciais
chaves_salvas = carregar_dados()
saldo_simulado = 5000

@app.route("/")
def home():
    return redirect("/painel")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("usuario") == "admin" and request.form.get("senha") == "claraverse2025":
            session["usuario"] = "admin"
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
    return render_template("configurar.html", chaves=chaves_salvas)

@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    data = request.json
    chaves_salvas["binance_api_key"] = data.get("binance_api_key", "")
    chaves_salvas["binance_api_secret"] = data.get("binance_api_secret", "")
    chaves_salvas["openai_api_key"] = data.get("openai_api_key", "")
    salvar_dados(chaves_salvas)
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

        openai.api_key = chaves_salvas["openai_api_key"]
        prompt = f"O preço atual do BTC é {preco}, com variação de {variacao}%. RSI em {rsi}. Qual a melhor sugestão para operação agora?"
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
            "sugestao": "Erro ao carregar dados da IA."
        })

@app.route("/executar/<acao>", methods=["POST"])
def executar_acao(acao):
    global saldo_simulado
    resposta = ""
    if acao == "entrada":
        resposta = "✅ ENTRADA realizada com sucesso."
    elif acao == "stop":
        saldo_simulado -= 100
        resposta = "🛑 STOP acionado. Proteção ativada."
    elif acao == "alvo":
        saldo_simulado += 150
        resposta = "🎯 ALVO atingido! Parabéns!"
    elif acao == "executar":
        resposta = "🚀 EXECUTAR: ordem enviada."
    elif acao == "automatico":
        resposta = "🤖 AUTOMÁTICO: Clarinha assumiu o controle."

    return jsonify({"mensagem": resposta, "novo_saldo": saldo_simulado})

# Render compat
application = app