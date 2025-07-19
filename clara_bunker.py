#CLARA BUNKER - Plataforma Inteligente Completa

from flask import Flask, render_template_string, request, jsonify
import requests, hmac, hashlib, time, base64, os

app = Flask(__name__)

# --- CHAVES BLINDADAS (exemplo protegidas, substituir pelas reais criptografadas) ---
API_KEY = "cfx-8c9e..."
API_SECRET = "9cf3e..."

# --- HTMLs Integrados ---
fachada_html = '''<!DOCTYPE html><html><head><title>ClaraVerse</title></head><body><h1>Fachada ClaraVerse</h1><a href="/sala">Ir para Sala de Operações</a></body></html>'''
sala_html = '''<!DOCTYPE html><html><head><title>Sala</title></head><body><h2>Sala de Operações</h2><form action="/executar" method="post"><input name="par" placeholder="BTCUSDT"><input name="valor" placeholder="Valor"><button>Executar Ordem</button></form></body></html>'''
config_html = '''<!DOCTYPE html><html><head><title>Configurações</title></head><body><h2>Configuração</h2><form action="/configurar" method="post"><input name="meta" placeholder="Meta"><button>Salvar</button></form></body></html>'''

@app.route("/")
def fachada():
    return render_template_string(fachada_html)

@app.route("/sala")
def sala():
    return render_template_string(sala_html)

@app.route("/config")
def config():
    return render_template_string(config_html)

@app.route("/executar", methods=["POST"])
def executar():
    par = request.form["par"]
    valor = request.form["valor"]
    timestamp = int(time.time() * 1000)
    query = f"symbol={par}&side=BUY&type=MARKET&quantity={valor}&timestamp={timestamp}"
    signature = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    headers = {"X-MBX-APIKEY": API_KEY}
    url = f"https://fapi.binance.com/fapi/v1/order?{query}&signature={signature}"
    r = requests.post(url, headers=headers)
    return jsonify(r.json())

@app.route("/configurar", methods=["POST"])
def configurar():
    meta = request.form["meta"]
    return f"Meta de lucro configurada: {meta}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    