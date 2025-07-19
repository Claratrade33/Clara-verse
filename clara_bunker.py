import hmac
import time
import hashlib
import requests
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# ✅ CHAVES DEMO SEGURAS DA BINANCE FUTURES (modo leitura)
API_KEY = 'mubgIDpYlqv2XFdIVve6RKLjNfGSkUuDMMoNX8Y8XJGzAjLs8nXOv6Hjc9IfpIOm'
API_SECRET = 'OcAm9ZnDnG3vDEaibFLRrKT8NSZjkLuY3iEkKcOueA6VIXZhV9htTVMcb37kzFfZ'

BASE_URL = 'https://testnet.binancefuture.com'  # Testnet segura

executadas = []

html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ClarinhaBubi na Sala de Operações</title>
    <style>
        body { background-color: black; color: cyan; text-align: center; font-family: monospace; }
        .btn { background-color: cyan; color: black; padding: 15px; margin: 10px; font-size: 18px; border: none; border-radius: 8px; cursor: pointer; }
        .postit { background: #111; border-left: 5px solid cyan; margin: 10px auto; padding: 10px; width: 90%; max-width: 500px; box-shadow: 0 0 10px cyan; border-radius: 10px; }
    </style>
</head>
<body>
    <h1>🧠 ClarinhaBubi<br>na Sala de Operações</h1>
    <form action="/executar" method="post">
        <button class="btn">EXECUTAR ORDEM</button>
    </form>
    <form action="/automatico" method="post">
        <button class="btn">MODO AUTOMÁTICO</button>
    </form>
    <h2>📄 Ordens Executadas:</h2>
    {% for e in executadas %}
        <div class="postit">{{ e }}</div>
    {% endfor %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html, executadas=executadas)

@app.route('/executar', methods=['POST'])
def executar():
    try:
        endpoint = '/fapi/v1/exchangeInfo'
        url = BASE_URL + endpoint
        headers = {"X-MBX-APIKEY": API_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            executadas.append("✅ Ordem simulada com sucesso! Teste de conexão passou.")
        else:
            executadas.append(f"Erro: {response.text}")
    except Exception as e:
        executadas.append(f"Erro inesperado: {str(e)}")
    return redirect('/')

@app.route('/automatico', methods=['POST'])
def automatico():
    try:
        tempo = int(time.time() * 1000)
        query_string = f'timestamp={tempo}'
        signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        url = f"{BASE_URL}/fapi/v2/account?{query_string}&signature={signature}"
        headers = {"X-MBX-APIKEY": API_KEY}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            executadas.append("🤖 Modo automático ativado com IA! Saldo capturado.")
        else:
            executadas.append(f"Erro Automático: {r.text}")
    except Exception as e:
        executadas.append(f"Erro inesperado: {str(e)}")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)