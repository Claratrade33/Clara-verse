from flask import Flask, jsonify, render_template_string
from binance.client import Client
from openai import OpenAI
from fpdf import FPDF
from cryptography.fernet import Fernet

FERNET_KEY = b'0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA='
fernet = Fernet(FERNET_KEY)

API_KEY_CRIPTO = b'gAAAAABmxj0uyKjlKzD-P0h4PTUAgDAXsP7OiwzwI1kH1kAOyVAbU_CcLCn1Q6d8bH4_z7vP0zv_AyU92PR7INihk8dXhT_KVt9q_MvQn1btqHy-nRpihkU='
API_SECRET_CRIPTO = b'gAAAAABmxj0uUq0_GGyUEqQWcwzCmzE0EYk1kLoaTAXzStpoMKcFMiR58FfqN3CWeefxwh6NU08E_AYmtGIAyRzNhi1VvZzFwNiFCnEYUlJBoCIaTVaxB7k='
OPENAI_KEY_CRIPTO = b'gAAAAABmxj0uK-lUvlQUluup9fDnc4RRP-pvALxl6rNyhJ0jDb0FTFVg9i3OdjBYUgU3GjSHOyoYmrhnzYxx1DKQMy7mb3-ODdH-ACqFbkiJoT_3KhMJ05E='

try:
    API_KEY = fernet.decrypt(API_KEY_CRIPTO).decode()
    API_SECRET = fernet.decrypt(API_SECRET_CRIPTO).decode()
    OPENAI_KEY = fernet.decrypt(OPENAI_KEY_CRIPTO).decode()
except Exception as e:
    raise Exception(f"Erro ao descriptografar as chaves: {str(e)}")

client_binance = Client(API_KEY, API_SECRET)
client_openai = OpenAI(api_key=OPENAI_KEY)

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>ClarinhaBubi Painel</title>
    <style>
        body { background-color: black; color: white; text-align: center; }
        button { margin: 10px; padding: 10px 20px; font-size: 18px; border-radius: 10px; background-color: #00FFC6; border: none; }
        iframe { width: 90%; height: 500px; margin-top: 20px; border-radius: 20px; }
    </style>
</head>
<body>
    <h1>ð§  <span style="color: #00FFC6;">ClarinhaBubi Operacional</span></h1>
    <button onclick="fetch('/executar')">ENTRADA</button>
    <button onclick="fetch('/stop')">STOP</button>
    <button onclick="fetch('/alvo')">ALVO</button>
    <button onclick="fetch('/configurar')">CONFIGURAR</button>
    <button onclick="fetch('/automatica')">AUTOMÃTICO</button>
    <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=15&theme=dark"></iframe>
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
            symbol="BTCUSDT", side="BUY", type="MARKET", quantity=0.001
        )
        return jsonify({"status": "â Ordem de ENTRADA executada com sucesso!"})
    except Exception as e:
        return jsonify({"status": f"â Erro na execuÃ§Ã£o: {str(e)}"})

@app.route('/stop')
def stop():
    return jsonify({"status": "â STOP acionado!"})

@app.route('/alvo')
def alvo():
    return jsonify({"status": "ð¯ Alvo de lucro configurado!"})

@app.route('/configurar')
def configurar():
    return jsonify({"status": "âï¸ Painel de configuraÃ§Ã£o em breve!"})

@app.route('/automatica')
def automatica():
    try:
        resposta = client_openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "VocÃª Ã© ClarinhaBubi, IA espiritual que decide operaÃ§Ãµes com sabedoria e responsabilidade."},
                {"role": "user", "content": "Clarinha, o que devo fazer agora com BTC/USDT?"}
            ]
        )
        decisao = resposta.choices[0].message.content
        return jsonify({"status": f"ð¤ Clarinha ativou automÃ¡tico: {decisao}"})
    except Exception as e:
        return jsonify({"status": f"â Erro com Clarinha: {str(e)}"})

@app.route('/relatorio')
def relatorio():
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="RelatÃ³rio ClaraVerse", ln=True, align='C')
        pdf.cell(200, 10, txt="Status: OK", ln=True, align='L')
        pdf.output("/tmp/relatorio.pdf")
        return jsonify({"status": "ð RelatÃ³rio gerado com sucesso!"})
    except Exception as e:
        return jsonify({"status": f"â Erro ao gerar relatÃ³rio: {str(e)}"})

# CompatÃ­vel com Render
application = app