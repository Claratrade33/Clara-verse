from flask import Flask, render_template, request, redirect, session, jsonify
import requests, os, openai
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 🔐 Credenciais
USUARIO_PADRAO = "admin"
SENHA_PADRAO = "claraverse2025"

# 🔒 Chave de criptografia (armazenada internamente)
fernet_key = Fernet.generate_key()
fernet = Fernet(fernet_key)

# 💾 Armazenamento seguro das chaves (criptografadas)
chaves_criptografadas = {
    "binance_api_key": "",
    "binance_api_secret": "",
    "openai_api_key": ""
}

# 💰 Saldo simulado
saldo_simulado = 5000.00

@app.route("/")
def home():
    return redirect("/painel")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        if usuario == USUARIO_PADRAO and senha == SENHA_PADRAO:
            session["usuario"] = usuario
            return redirect("/painel")
        return render_template("login.html", erro="Credenciais inválidas.")
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
    return render_template("configurar.html", chaves={k: "[PROTEGIDO]" for k in chaves_criptografadas})

@app.route("/painel")
def painel():
    if "usuario" not in session:
        return redirect("/login")
    return render_template("painel.html", chaves={k: "[PROTEGIDO]" for k in chaves_criptografadas}, saldo=saldo_simulado)

@app.route("/salvar_chaves", methods=["POST"])
def salvar_chaves():
    data = request.json
    for key in chaves_criptografadas:
        valor = data.get(key, "")
        chaves_criptografadas[key] = fernet.encrypt(valor.encode()).decode()
    return jsonify({"status": "sucesso"})

@app.route("/dados_mercado")
def dados_mercado():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
        r = requests.get(url).json()
        preco = float(r.get("lastPrice", 0))
        variacao = float(r.get("priceChangePercent", 0))
        volume = float(r.get("quoteVolume", 0))

        # RSI e Níveis
        rsi = round(50 + variacao / 2, 2)
        suporte = round(preco * 0.98, 2)
        resistencia = round(preco * 1.02, 2)

        # IA GPT
        chave_openai = fernet.decrypt(chaves_criptografadas["openai_api_key"].encode()).decode()
        openai.api_key = chave_openai

        prompt = f"""
        O preço atual do BTC é {preco}, com variação de {variacao}%, RSI em {rsi}, suporte em {suporte}, resistência em {resistencia}.
        Com base nisso, qual a melhor estratégia neste momento? Responda com clareza e de forma prática.
        """

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
            "sugestao": "Erro ao buscar dados ou resposta da IA."
        })

@app.route("/executar/<acao>", methods=["POST"])
def executar_acao(acao):
    global saldo_simulado
    mensagens = {
        "entrada": "Entrada confirmada! Operação iniciada.",
        "stop": "Stop ativado. Saída com proteção.",
        "alvo": "Alvo atingido! Lucro realizado.",
        "automatico": "Modo automático ativado. A IA está operando por você.",
        "executar": "Ordem executada com base na análise da Clarinha."
    }
    # Simula pequena variação no saldo
    if acao == "entrada":
        saldo_simulado -= 50
    elif acao == "alvo":
        saldo_simulado += 100
    elif acao == "stop":
        saldo_simulado -= 30

    return jsonify({
        "mensagem": mensagens.get(acao, "Ação desconhecida."),
        "saldo": round(saldo_simulado, 2)
    })

# 🔁 Compatibilidade com Render
application = app