# clara_bunker.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests, hmac, hashlib, time, base64
from cryptography.fernet import Fernet

app = Flask(__name__)
application = app  # Necessário para o Render

# ===🔐 CONFIGURAÇÃO DAS CHAVES PROTEGIDAS===
FERNET_KEY = b'0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA='  # Chave fernet
fernet = Fernet(FERNET_KEY)

API_KEY_CRYPT = "Z1axmcmEQF1mrgYKiZwY4w=="  # Exemplo real criptografado (deve substituir pela sua versão criptografada correta)
SECRET_KEY_CRYPT = "g3fEgf+EXAMPLEx2ncd0=="  # Idem

def decrypt_key(encrypted):
    return fernet.decrypt(encrypted.encode()).decode()

try:
    API_KEY = decrypt_key(API_KEY_CRYPT)
    API_SECRET = decrypt_key(SECRET_KEY_CRYPT)
except Exception as e:
    print("Erro ao descriptografar as chaves:", e)
    API_KEY = API_SECRET = ""

# ===⚙️ FUNÇÕES DE OPERAÇÃO REAL BINANCE===
def gerar_assinatura(query_string, secret):
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def criar_ordem_binance(symbol, side, quantity, leverage):
    url = "https://fapi.binance.com/fapi/v1/order"
    timestamp = int(time.time() * 1000)
    params = f"symbol={symbol}&side={side}&type=MARKET&quantity={quantity}&timestamp={timestamp}"
    signature = gerar_assinatura(params, API_SECRET)
    headers = {"X-MBX-APIKEY": API_KEY}
    full_url = f"{url}?{params}&signature={signature}"
    response = requests.post(full_url, headers=headers)
    return response.json()

# ===🧠 INTELIGÊNCIA CLARINHA===
def clarinha_decide(moeda, tendencia):
    if tendencia == "alta":
        return "BUY"
    elif tendencia == "baixa":
        return "SELL"
    return "BUY"

# ===🔁 ROTAS ===
@app.route('/')
def fachada():
    return render_template("fachada.html")

@app.route('/sala-operacoes')
def sala_operacoes():
    return render_template("sala_operacoes.html")

@app.route('/configuracoes', methods=["GET", "POST"])
def configuracoes():
    if request.method == "POST":
        meta = request.form.get("meta")
        modo = request.form.get("modo")
        return redirect(url_for('sala_operacoes'))
    return render_template("painel_configuracoes.html")

@app.route('/executar', methods=["POST"])
def executar_ordem():
    dados = request.json
    moeda = dados.get("moeda", "BTCUSDT")
    tendencia = dados.get("tendencia", "alta")
    quantidade = float(dados.get("quantidade", 0.001))
    alavancagem = int(dados.get("alavancagem", 1))
    modo = dados.get("modo", "auto")

    if modo == "auto":
        direcao = clarinha_decide(moeda, tendencia)
    else:
        direcao = dados.get("direcao_manual", "BUY")

    resultado = criar_ordem_binance(moeda, direcao, quantidade, alavancagem)
    return jsonify(resultado)

# ===📊 ROTA PARA GRÁFICO E ROI===
@app.route('/grafico')
def grafico():
    return render_template("grafico.html")

# ===🔥 EXECUÇÃO ===
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)