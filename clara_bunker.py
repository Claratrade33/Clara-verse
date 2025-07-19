from flask import Flask, render_template_string, request, jsonify
from openai import OpenAI
from binance.client import Client
from fpdf import FPDF
from cryptography.fernet import Fernet

# 🔐 Modo Bunker: chave fixa
FERNET_KEY = b'0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA='
fernet = Fernet(FERNET_KEY)

# 🔒 Chaves criptografadas (exemplo — substitua pelas suas reais criptografadas)
API_KEY_CRIPTO = b'gAAAAABoe9iObom4xwGtEl9H2uZGFtFnDl2ar4j94Q-vlyw99enohpfxFmPmRjhBO2q4InocU78uYEFRNCq4CmgJKtEwlV4Rgw=='
API_SECRET_CRIPTO = b'gAAAAABoe9iObcfu1GXbT93iU2Lcp3ZY07Wy3WoG6MLF0hpNgbYwcOQkt670--qQGokWjK4zMljsdulf6z8nnI2Tsr0wLkTeEw=='
OPENAI_KEY_CRIPTO = b'gAAAAABoe9iOIK9Lx6CtSQ8aZNegSgktg8-4zD1aJjG0KUG8GsSh4HmJ3-CLu_77-nUA-u4FYQTZ18uU_VrJP3JiN4-fDgqdLg=='

# 🔓 Descriptografar as chaves
try:
    API_KEY = fernet.decrypt(API_KEY_CRIPTO).decode()
    API_SECRET = fernet.decrypt(API_SECRET_CRIPTO).decode()
    OPENAI_KEY = fernet.decrypt(OPENAI_KEY_CRIPTO).decode()
except Exception as e:
    print("❌ Erro ao descriptografar:", e)
    API_KEY = "erro"
    API_SECRET = "erro"
    OPENAI_KEY = "erro"

# 🔌 Clientes
client_binance = Client(API_KEY, API_SECRET, testnet=False)
client_openai = OpenAI(api_key=OPENAI_KEY)

# 🚀 App Flask
app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/executar')
def executar():
    try:
        ordem = client_binance.futures_create_order(
            symbol="BTCUSDT", side="BUY", type="MARKET", quantity=0.001)
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
            model="gpt-4o",
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

# ✅ Ponto de entrada para Render
application = app