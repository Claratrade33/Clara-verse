from flask import Flask, render_template, request, redirect, session, jsonify
import os, requests, openai, json
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 👤 Login padrão
USUARIO_PADRAO = "admin"
SENHA_PADRAO = "claraverse2025"

# 💰 Saldo simulado
saldo_simulado = 5000.00

# 🔐 Segurança: criptografia Fernet
chave_fernet_path = "chave_fernet.key"
arquivo_chaves = "chaves_segredas.json"

if not os.path.exists(chave_fernet_path):
    with open(chave_fernet_path, "wb") as f:
        f.write(Fernet.generate_key())

with open(chave_fernet_path, "rb") as f:
    fernet = Fernet(f.read())

def carregar_chaves():
    if os.path.exists(arquivo_chaves):
        with open(arquivo_chaves, "rb") as f:
            criptografado = f.read()
        try:
            return json.loads(fernet.decrypt(criptografado).decode())
        except:
            return {"binance_api_key": "", "binance_api_secret": "", "openai_api_key": ""}
    return {"binance_api_key": "", "binance_api_secret": "", "openai_api_key": ""}

def salvar_chaves_local(chaves):
    dados = json.dumps(chaves).encode()
    with open(arquivo_chaves, "wb") as f:
        f.write(fernet.encrypt(dados))

# 🔐 Carrega as chaves salvas
chaves_salvas = carregar_chaves()

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

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/configurar")
def configurar():
    if "usuario" not in session:
        return redirect("/login")
    return render_template("configurar.html", chaves=chaves_salvas)

@app.route("/painel")
def painel():
    if "usuario" not in session:
        return redirect("/login")
    return render_template("painel.html", chaves=chaves_salvas, saldo=saldo_simulado)

@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    data = request.json
    chaves_salvas.update({
        "binance_api_key": data.get("binance_api_key", ""),
        "binance_api_secret": data.get("binance_api_secret", ""),
        "openai_api_key": data.get("openai_api_key", "")
    })
    salvar_chaves_local(chaves_salvas)
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

        # ⚙️ GPT com chave configurada
        openai.api_key = chaves_salvas["openai_api_key"]
        prompt = f"O preço atual do BTC é {preco}, com variação de {variacao}%. RSI em {rsi}. Suporte em {suporte} e resistência em {resistencia}. Qual a melhor sugestão de operação?"
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
            "sugestao": "Erro ao carregar dados."
        })

@app.route("/executar/<acao>", methods=["POST"])
def executar_acao(acao):
    global saldo_simulado
    acoes = {
        "entrada": "Entrada efetuada com sucesso.",
        "stop": "STOP acionado. Proteção ativada.",
        "alvo": "ALVO alcançado. Operação encerrada.",
        "executar": "Ordem executada com base na análise da IA.",
        "automatico": "Modo automático ativado. Clarinha está no comando."
    }
    # Exemplo de simulação de saldo
    if acao == "entrada":
        saldo_simulado -= 100
    elif acao == "alvo":
        saldo_simulado += 150
    elif acao == "stop":
        saldo_simulado -= 80
    msg = acoes.get(acao, "Ação desconhecida.")
    return jsonify({"mensagem": msg, "novo_saldo": round(saldo_simulado, 2)})

# 🌐 Compatibilidade com Render
application = app