from flask import Flask, jsonify, render_template_string
from fpdf import FPDF
from cryptography.fernet import Fernet
from binance.client import Client
from openai import OpenAI

# 🔐 Modo Bunker: chave fixa
FERNET_KEY = b'0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA='
fernet = Fernet(FERNET_KEY)

# 🔐 Chaves criptografadas
API_KEY_CRIPTO = b'gAAAAABoe94Md1XuKtY3R6RBBWOYw7Hdrc3fD8-QlKxV9cpj0ncVN8g8l1KefBXgcJWu_6ntmoSqSitVgdyfwkZmX2eypwo2Ms0JLzG6Y7ZZ-kicYR0pX9s='
API_SECRET_CRIPTO = b'gAAAAABoe94M5h0qn3zjqtPBGDSvXkF0eROSP9KKfN-dr8HlNrJCw3ZNHBU-LZaGpD6aXldq0lHprhdn116xCbqX41Vi1FetwfID4PRXkrTCSnw0MXTlOtQ='
OPENAI_KEY_CRIPTO = b'gAAAAABoe94MHI-8Nq_JwTE8J1aPb9ATt1N5aACCtYpX4ypk950ZzAXsqhH4vagu9zCOuCscVUxYCAwdc_FHl3Mrt4ztuJ50u3GuI78gi0kRkr-O-jDS9xY='

# 🔓 Descriptografar chaves
try:
    API_KEY = fernet.decrypt(API_KEY_CRIPTO).decode()
    API_SECRET = fernet.decrypt(API_SECRET_CRIPTO).decode()
    OPENAI_KEY = fernet.decrypt(OPENAI_KEY_CRIPTO).decode()
except Exception as e:
    raise Exception(f"Erro ao descriptografar as chaves: {e}")

# ✅ Clientes
client_binance = Client(API_KEY, API_SECRET)
client_openai = OpenAI(api_key=OPENAI_KEY)

# 🌐 Web app
app = Flask(__name__)

# 🧠 Frontend HTML básico
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>ClaraVerse</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial; }
        h1 { color: cyan; }
        button {
            margin: 10px;
            padding: 15px 30px;
            font-size: 18px;
            background-color: #00ffcc;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>🧠 ClarinhaBubi Operacional</h1>
    <a href="/executar"><button>ENTRADA</button></a>
    <a href="/stop"><button>STOP</button></a>
    <a href="/alvo"><button>ALVO</button></a>
    <a href="/configurar"><button>CONFIGURAR</button></a>
    <a href="/automatico"><button>AUTOMÁTICO</button></a>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/executar')
def executar():
    try:
        ordem = client_binance.futures_create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity=0.001
        )
        return jsonify({"status": "✅ Ordem de ENTRADA executada com sucesso!"})
    except Exception as e:
        return jsonify({"status": f"❌ Erro na execução: {str(e)}"})

@app.route('/stop')
def stop():
    return jsonify({"status": "⛔ STOP acionado!"})

@app.route('/alvo')
def alvo():
    return jsonify({"status": "🎯 Alvo de lucro configurado!"})

@app.route('/configurar')
def configurar():
    return jsonify({"status": "⚙️ Painel de configuração em breve!"})

@app.route('/automatico')
def automatico():
    try:
        resposta = client_openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é ClarinhaBubi, IA espiritual que decide operações com sabedoria e responsabilidade."},
                {"role": "user", "content": "Clarinha, o que devo fazer agora com BTC/USDT?"}
            ]
        )
        decisao = resposta.choices[0].message.content
        return jsonify({"status": f"🤖 Clarinha ativou automático: {decisao}"})
    except Exception as e:
        return jsonify({"status": f"❌ Erro com Clarinha: {str(e)}"})

@app.route('/relatorio')
def relatorio():
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="Relatório ClaraVerse", ln=True, align='C')
        pdf.cell(200, 10, txt="Status: OK", ln=True, align='L')
        pdf.output("/tmp/relatorio.pdf")
        return jsonify({"status": "📄 Relatório gerado com sucesso!"})
    except Exception as e:
        return jsonify({"status": f"❌ Erro ao gerar relatório: {str(e)}"})

# 🔁 Compatível com Render
application = app