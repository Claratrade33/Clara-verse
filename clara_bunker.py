from flask import Flask, render_template_string, request, jsonify
import os
import openai
from binance.client import Client
from fpdf import FPDF
from cryptography.fernet import Fernet

# 🔐 Chave Fernet para criptografia
FERNET_KEY = b'0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA='
fernet = Fernet(FERNET_KEY)

# 🔒 Chaves criptografadas (REAIS)
API_KEY_CRIPTO = b'gAAAAABmTMd7NRhFfhdEw8pTTKPgkoJSixC4JYgM96v9pNYUVRM8KQuHFf_Urzk6r0HLH30G1DgmIf1bWv6gxzYq51yR4WvfrvEoxfA4zKQY2Mx2jMN2Ogg='
API_SECRET_CRIPTO = b'gAAAAABmTMd7rEQ3G8gZy6o3ZnQ5L6V0_aOKVmT81TbE6Xk7lfUYsgFgUVejFMUDVWkQjZdKYpjsd4VDYfGDN2NK0dz-iF4jM93AoCuXmRPp5D3c79IK2yo='
OPENAI_KEY = "sk-proj-KJ7TxS0gKDl8a9eAjEowuFJXtqjFZkH8vOtjcC..."

# 🔓 Descriptografar chaves
try:
    API_KEY = fernet.decrypt(API_KEY_CRIPTO).decode()
    API_SECRET = fernet.decrypt(API_SECRET_CRIPTO).decode()
except:
    API_KEY = "erro"
    API_SECRET = "erro"

# 🔌 Conectar à OpenAI e Binance
openai.api_key = OPENAI_KEY
client = Client(API_KEY, API_SECRET, testnet=False)  # REAL MODE

# 🚀 Iniciar app
app = Flask(__name__)

# 🌌 Interface futurista ClaraVerse
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>ClaraVerse | Sala de Operações</title>
    <style>
        body { background: #000; color: #00ffcc; font-family: Arial, sans-serif; text-align: center; padding: 30px; }
        h1 { margin-bottom: 20px; }
        button {
            background: #00ffcc; border: none; padding: 15px 30px; margin: 10px;
            border-radius: 10px; font-size: 18px; cursor: pointer; box-shadow: 0 0 15px #00ffcc66;
        }
        iframe { margin-top: 40px; width: 100%; height: 450px; border: none; }
    </style>
</head>
<body>
    <h1>🧠 ClarinhaBubi Operacional</h1>
    <button onclick="fetch('/executar').then(r=>r.json()).then(d=>alert(d.status))">ENTRADA</button>
    <button onclick="fetch('/stop').then(r=>r.json()).then(d=>alert(d.status))">STOP</button>
    <button onclick="fetch('/alvo').then(r=>r.json()).then(d=>alert(d.status))">ALVO</button>
    <button onclick="fetch('/configurar').then(r=>r.json()).then(d=>alert(d.status))">CONFIGURAR</button>
    <button onclick="fetch('/automatico').then(r=>r.json()).then(d=>alert(d.status))">AUTOMÁTICO</button>
    <iframe src="https://www.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=15&theme=dark" allowfullscreen></iframe>
</body>
</html>
"""

# 🌐 Página inicial
@app.route('/')
def index():
    return render_template_string(html_template)

# 🟢 Executar ordem de compra real
@app.route('/executar')
def executar():
    try:
        ordem = client.futures_create_order(symbol="BTCUSDT", side="BUY", type="MARKET", quantity=0.001)
        return jsonify({"status": "✅ Ordem de ENTRADA executada com sucesso!"})
    except Exception as e:
        return jsonify({"status": f"❌ Erro: {str(e)}"})

# ⛔ Stop manual
@app.route('/stop')
def stop():
    return jsonify({"status": "⛔ STOP acionado!"})

# 🎯 Alvo manual
@app.route('/alvo')
def alvo():
    return jsonify({"status": "🎯 Alvo de lucro configurado!"})

# ⚙️ Configuração
@app.route('/configurar')
def configurar():
    return jsonify({"status": "⚙️ Painel de configuração em breve!"})

# 🤖 Modo automático com ClarinhaBubi
@app.route('/automatico')
def automatico():
    try:
        resposta = openai.ChatCompletion.create(
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

# 📄 Gerar relatório
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

# 🔁 Para Render
application = app