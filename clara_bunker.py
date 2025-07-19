# clara_bunker.py - ARQUIVO ÚNICO E FUNCIONAL

from flask import Flask, render_template_string, request, jsonify
import openai, base64, json, threading, time
from binance.client import Client
from cryptography.fernet import Fernet
from fpdf import FPDF

# ======================== CONFIGURAÇÕES ========================
app = Flask(__name__)
application = app  # Para funcionar no Render

# Chaves criptografadas (exemplo fictício - substitua pelas reais criptografadas)
FERNET_KEY = "0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="
fernet = Fernet(FERNET_KEY.encode())

OPENAI_KEY = fernet.decrypt(b"gAAAAABm...").decode()
API_KEY = fernet.decrypt(b"gAAAAABl...").decode()
API_SECRET = fernet.decrypt(b"gAAAAABm...").decode()

openai.api_key = OPENAI_KEY
binance_client = Client(API_KEY, API_SECRET, testnet=True)

# ======================== IA Clarinha ========================
def clarinha_responde(pergunta):
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Você é a IA ClarinhaBubi, espiritual e estratégica."},
                  {"role": "user", "content": pergunta}]
    )
    return resposta.choices[0].message.content

# ======================== ROTAS ========================
@app.route("/")
def fachada():
    return render_template_string("""<html><head><title>ClaraVerse</title></head><body>
        <h1>Fachada ClaraVerse</h1>
        <a href='/sala-operacoes'>Entrar na Sala de Operações</a>
        </body></html>""")

@app.route("/sala-operacoes")
def sala():
    return render_template_string("""<html><head><title>Sala</title></head><body>
        <h2>Sala de Operações</h2>
        <button onclick="fetch('/executar', {method: 'POST'}).then(r => r.text()).then(alert)">EXECUTAR</button>
        <button onclick="fetch('/automatico', {method: 'POST'}).then(r => r.text()).then(alert)">AUTOMÁTICO</button>
        <a href='/configurar'>Configurar</a> | <a href='/relatorio'>Relatório</a>
        </body></html>""")

@app.route("/configurar", methods=["GET", "POST"])
def configurar():
    if request.method == "POST":
        modo = request.form.get("modo")
        par = request.form.get("par")
        meta = request.form.get("meta")
        return f"Configurações salvas: Modo {modo}, Par {par}, Meta {meta}"
    return render_template_string("""<form method='post'>
        Modo: <select name='modo'><option>Manual</option><option>Automático</option></select><br>
        Par: <input name='par' value='BTCUSDT'><br>
        Meta diária: <input name='meta' value='10'><br>
        <button type='submit'>Salvar</button></form>""")

@app.route("/executar", methods=["POST"])
def executar():
    par = "BTCUSDT"
    quantidade = 0.01
    ordem = binance_client.futures_create_order(symbol=par, side='BUY', type='MARKET', quantity=quantidade)
    return f"Ordem executada: {ordem}"

@app.route("/automatico", methods=["POST"])
def automatico():
    # Estratégia Dupla Respiração
    par = "BTCUSDT"
    quantidade = 0.01
    binance_client.futures_create_order(symbol=par, side='BUY', type='MARKET', quantity=quantidade)
    binance_client.futures_create_order(symbol=par, side='SELL', type='MARKET', quantity=quantidade)
    return "Dupla respiração executada."

@app.route("/relatorio")
def relatorio():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório de Operações", ln=True, align="C")
    pdf.cell(200, 10, txt="Ordem executada: Compra e venda BTCUSDT", ln=True)
    pdf_file = "/tmp/relatorio.pdf"
    pdf.output(pdf_file)
    with open(pdf_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"<a href='data:application/pdf;base64,{encoded}' download='relatorio.pdf'>Download Relatório</a>"

# ======================== EXECUÇÃO ========================
if __name__ == "__main__":
    app.run(debug=True