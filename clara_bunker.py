from flask import Flask, render_template, request, redirect, session, jsonify
import requests, os, openai, json

app = Flask(__name__)
app.secret_key = os.urandom(24)

USUARIO_PADRAO = "admin"
SENHA_PADRAO = "claraverse2025"

# Arquivo local para persistência
ARQUIVO_CHAVES = "chaves_claraverse.json"

# Carregar chaves salvas
if os.path.exists(ARQUIVO_CHAVES):
    with open(ARQUIVO_CHAVES, "r") as f:
        chaves_salvas = json.load(f)
else:
    chaves_salvas = {
        "binance_api_key": "",
        "binance_api_secret": "",
        "openai_api_key": ""
    }

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
    return render_template("painel.html", chaves=chaves_salvas, saldo=5000)

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
    with open(ARQUIVO_CHAVES, "w") as f:
        json.dump(chaves_salvas, f)
    return jsonify({"status": "sucesso", "redirect": "/painel"})

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

        openai.api_key = chaves_salvas.get("openai_api_key", "")
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
            "sugestao": "Erro ao carregar dados ou IA não respondeu."
        })

@app.route("/executar/<acao>", methods=["POST"])
def executar_acao(acao):
    acoes = {
        "entrada": "Ordem de ENTRADA simulada com sucesso.",
        "stop": "STOP ativado! Proteção acionada.",
        "alvo": "ALVO definido e operação encerrada.",
        "automatico": "Modo automático ativado. Clarinha vai operar por você.",
        "executar": "Ordem executada conforme análise da IA."
    }
    msg = acoes.get(acao, "Ação desconhecida.")
    return jsonify({"mensagem": msg})

# Compatibilidade Render
application = app