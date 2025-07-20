from flask import Flask, render_template, request, redirect, session, jsonify
import requests, os, openai, json
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Geração de chave secreta para criptografia
KEY_FILE = "chave_secreta.key"
DATA_FILE = "dados_criptografados.json"

if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "wb") as f:
        f.write(Fernet.generate_key())

with open(KEY_FILE, "rb") as f:
    cipher = Fernet(f.read())

# Saldo simulado
saldo_simulado = 5000.0

# Carregar dados salvos criptografados
def carregar_chaves():
    if not os.path.exists(DATA_FILE):
        return {"binance_api_key": "", "binance_api_secret": "", "openai_api_key": ""}
    with open(DATA_FILE, "rb") as f:
        try:
            decrypted_data = cipher.decrypt(f.read()).decode()
            return json.loads(decrypted_data)
        except:
            return {"binance_api_key": "", "binance_api_secret": "", "openai_api_key": ""}

# Salvar dados criptografados
def salvar_chaves_seguras(dados):
    with open(DATA_FILE, "wb") as f:
        criptografado = cipher.encrypt(json.dumps(dados).encode())
        f.write(criptografado)

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
    chaves = carregar_chaves()
    return render_template("painel.html", saldo=saldo_simulado, chaves=chaves)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/configurar")
def configurar():
    if "usuario" not in session:
        return redirect("/login")
    chaves = carregar_chaves()
    return render_template("configurar.html", chaves=chaves)

@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    data = request.get_json()
    salvar_chaves_seguras({
        "binance_api_key": data.get("binance_api_key", ""),
        "binance_api_secret": data.get("binance_api_secret", ""),
        "openai_api_key": data.get("openai_api_key", "")
    })
    return jsonify({"status": "sucesso"})

@app.route("/dados_mercado")
def dados_mercado():
    chaves = carregar_chaves()
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
        r = requests.get(url).json()
        preco = r.get("lastPrice", "--")
        variacao = r.get("priceChangePercent", "--")
        volume = r.get("quoteVolume", "--")

        rsi = round(50 + float(variacao)/2, 2)
        suporte = round(float(variacao) - 0.8, 2)
        resistencia = round(float(variacao) + 0.8, 2)

        openai.api_key = chaves.get("openai_api_key")
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
    acoes = {
        "entrada": "✅ Ordem de ENTRADA simulada!",
        "stop": "🛑 Stop acionado. Proteção ativada.",
        "alvo": "🎯 Alvo atingido! Operação encerrada.",
        "automatico": "🤖 Modo automático ativado.",
        "executar": "🚀 Ordem executada com base na IA."
    }
    if acao == "entrada":
        saldo_simulado -= 100
    elif acao == "alvo":
        saldo_simulado += 150
    elif acao == "stop":
        saldo_simulado -= 50
    return jsonify({"mensagem": acoes.get(acao, "Ação desconhecida.")})

# Compatível com Render
application = app