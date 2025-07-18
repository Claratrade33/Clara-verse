from flask import Flask, render_template, request, redirect, url_for, session, render_template_string
from flask_cors import CORS
import os
from dotenv import load_dotenv
import openai
from binance.client import Client

# ====== CONFIGURAÇÕES ======
load_dotenv()
app = Flask(__name__)
CORS(app)

app.secret_key = os.getenv("SECRET_KEY", "segredo_padrao")
openai.api_key = os.getenv("OPENAI")

# Binance modo testnet (demo)
api_key = os.getenv("Bia")
api_secret = os.getenv("Bia1")
client = Client(api_key, api_secret)
client.API_URL = 'https://testnet.binancefuture.com/fapi'

# Tokens permitidos
TOKENS_PERMITIDOS = ["ORIGEM", "VEUS", "DESPERTAR", "INFINITY", "SOMA", "ANJOS"]
LINHAS_REQUERIDAS = 8

# Saldo demo inicial
saldo_demo = {"USDT": 10000}

# ========= ROTAS =========

@app.route("/", methods=["GET", "POST"])
def index():
    login_template = """
    <html><head><title>ClaraVerse</title><style>
    body { background-color: black; color: lime; font-family: monospace; text-align: center; padding-top: 100px; }
    input { background: black; color: lime; border: 1px solid lime; padding: 10px; font-size: 18px; }
    </style></head><body>
    <h2>🔐 Acesso ClaraVerse</h2>
    <form method="POST">
        <input type="text" name="token" placeholder="Digite seu token de acesso">
        <br><br>
        <input type="submit" value="Entrar">
    </form>
    {% if erro %}<p style="color:red;">{{ erro }}</p>{% endif %}
    </body></html>
    """
    if request.method == "POST":
        token = request.form.get("token", "").strip().upper()
        if token in TOKENS_PERMITIDOS:
            session["token"] = token
            return redirect("/sala-operacoes")
        else:
            return render_template_string(login_template, linhas=LINHAS_REQUERIDAS, erro="Token inválido.")
    return render_template_string(login_template, linhas=LINHAS_REQUERIDAS, erro=None)

@app.route("/sala-operacoes")
def sala_operacoes():
    if "token" not in session:
        return redirect("/")
    return render_template("sala_operacoes.html", saldo=saldo_demo)

@app.route("/configuracoes", methods=["GET", "POST"])
def configuracoes():
    if "token" not in session or session["token"] != "SOMA":
        return redirect("/")
    if request.method == "POST":
        session["modo"] = request.form.get("modo")
        session["meta"] = request.form.get("meta")
        session["api"] = request.form.get("api")
        session["secret"] = request.form.get("secret")
        return redirect("/sala-operacoes")
    return render_template("painel_configuracoes.html")

@app.route("/executar-ordem", methods=["POST"])
def executar_ordem():
    par = request.form.get("par", "BTCUSDT")
    direcao = request.form.get("direcao", "buy")
    quantidade = float(request.form.get("quantidade", 10.0))

    preco_entrada = float(client.futures_mark_price(symbol=par)["markPrice"])
    lucro = round(quantidade * 0.02, 2)
    resultado = {
        "par": par,
        "direcao": direcao,
        "quantidade": quantidade,
        "preco": preco_entrada,
        "lucro": lucro,
        "roi": f"{round((lucro/quantidade)*100, 2)}%",
        "status": "executada"
    }
    return resultado

@app.route("/ativar-automatico", methods=["POST"])
def ativar_automatico():
    par = "BTCUSDT"
    preco = float(client.futures_mark_price(symbol=par)["markPrice"])
    tendencia = "alta" if float(preco) % 2 == 0 else "baixa"
    rsi = 50

    prompt = f"""
Você é a Clarinha, uma IA estratégica para operações na Binance.
Com base na tendência {tendencia}, RSI {rsi} e preço atual {preco}, diga se devo comprar ou vender e qual estratégia aplicar.
Responda de forma direta e clara.
"""
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    acao = resposta.choices[0].message["content"].strip()
    return {"resposta": acao}

# ========= INICIAR =========
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

application = app  # Render compatível