from flask import Flask, render_template, request, jsonify
from cryptography.fernet import Fernet
from binance.client import Client
from openai import OpenAI

# Chave usada para descriptografar os segredos
FERNET_KEY = "QnTaKpFbUzmM3N4qNtHEmV_BQ8-1tnbM36wNqM1U9Ko="
fernet = Fernet(FERNET_KEY.encode())

# Chaves criptografadas (já protegidas)
API_KEY = fernet.decrypt(b'gAAAAABofDghf9eSxqpOqsQkR-iewv6KZXcA2FWZOPf1ognDx6Y8g4-vF9V8Po-z6W-ydMf_ohYx2H9Upq5bJ-m5nQxvCuvY8oGT6TN7KnAFbzpimAWcE30=').decode()
API_SECRET = fernet.decrypt(b'gAAAAABofDghGlcu9ejy3yfnr_UwSIJ7A0lh57IkMOnYFskyIwvPiI_G4h3p5k6_GXwCOv31jsLcnKwve-iHnatMZS02pumeLZYa-PtnW8PIBrxucLeuwAM=').decode()
OPENAI_KEY = fernet.decrypt(b'gAAAAABofDgh3onD_TVObo3dm7H0I3oysxYvC3-1ZVHvhw0AM4oR_ZwmaLHSVKUaoYH2Joq4ayNUsJ47QaSW65Y-mvNYImGViw70oy-XjAvK6KeDEfTH63g=').decode()

# Inicialização
app = Flask(__name__)
binance = Client(API_KEY, API_SECRET)
client_openai = OpenAI(api_key=OPENAI_KEY)

# Página inicial: carrega o HTML separado
@app.route("/")
def index():
    return render_template("painel.html")

# Rota de análise
@app.route("/analise", methods=["POST"])
def analise():
    data = request.get_json()
    symbol = data.get("symbol", "BTCUSDT")

    # Busca de dados de mercado
    klines = binance.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=50)
    candles = [float(k[4]) for k in klines]
    prompt = f"""
Você é uma IA que analisa criptomoedas. Com base nos dados: {candles},
gere uma recomendação no seguinte formato JSON:

{{
  "entrada": "valor de entrada ideal",
  "stop": "valor de stop",
  "alvo": "valor de alvo",
  "confianca": "grau de confiança da análise (0 a 100)"
}}
"""

    resposta = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    try:
        conteudo = resposta.choices[0].message.content
        resultado = eval(conteudo) if conteudo.startswith("{") else {}
    except Exception:
        resultado = {
            "entrada": "Erro",
            "stop": "Erro",
            "alvo": "Erro",
            "confianca": "0"
        }

    return jsonify(resultado)

# Exporta para o Render
application = app
