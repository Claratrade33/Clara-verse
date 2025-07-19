import time
import requests
import threading
from flask import Flask, render_template_string, request, jsonify
from binance.client import Client
from binance.enums import *
from cryptography.fernet import Fernet

# Chave Fernet protegida (não altere)
FERNET_KEY = b"0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="
f = Fernet(FERNET_KEY)

# Chaves reais criptografadas
API_KEY_CIFRADA = b'gAAAAABoeyKfN1Oakb1dEgrA1BkRYnWl7sL6AwpT3O6g_geDi2Tjk00YJ54KLPHLxOHNta_WVTLtN1jUYC8Jm99-KHEcFNMtow84bAwGdugt8jgA5gv6oH9nEkECNSq5Z022GmQwMN3W9lEX4NezBPhs-f67Qy1mR3zjp131g0qsTTdpqXJT1vk='
API_SECRET_CIFRADA = b'gAAAAABoeyKf4GzLNWezTx2uCEx_kWr1a0CgIxuFeVXOicikwCZgXKARzbiqIxuXE1dDQik2XYJc5zTrRKkKzNXiWjT5clYPw6-P5DxCnWj0npCvhnGCKx16Fs7U-xR_8gUsBqU1EVeCWbj5ffoI5fkIUQzNK4ggJaWni3VbCbA9EV8kUoNq9wc='

# Descriptografar para uso
api_key = f.decrypt(API_KEY_CIFRADA).decode()
api_secret = f.decrypt(API_SECRET_CIFRADA).decode()

# Cliente Binance
client = Client(api_key, api_secret, testnet=False)

app = Flask(__name__)

ordens_executadas = []

# Rota principal com painel
@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Sala de Operações ClaraVerse</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                background-color: #000;
                color: #0ff;
                font-family: 'Courier New', monospace;
                padding: 20px;
                text-align: center;
            }
            h1 { color: #0ff; }
            button {
                background-color: #0ff;
                border: none;
                padding: 10px 20px;
                font-size: 18px;
                color: #000;
                margin: 10px;
                cursor: pointer;
                border-radius: 5px;
                box-shadow: 0 0 10px #0ff;
            }
            .ordem-postit {
                background: #111;
                border-left: 6px solid #0ff;
                color: #0ff;
                padding: 15px;
                margin: 10px auto;
                width: 90%;
                max-width: 500px;
                font-size: 16px;
                box-shadow: 0 0 10px #0ff4;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <h1>🧠 ClarinhaBubi na Sala de Operações</h1>
        <button onclick="fetch('/executar', {method: 'POST'}).then(() => location.reload())">EXECUTAR ORDEM</button>
        <button onclick="fetch('/automatica', {method: 'POST'}).then(() => location.reload())">MODO AUTOMÁTICO</button>
        <h2>📄 Ordens Executadas:</h2>
        {% for ordem in ordens %}
            <div class="ordem-postit">{{ ordem }}</div>
        {% endfor %}
    </body>
    </html>
    '''
    return render_template_string(html, ordens=ordens_executadas)

# Lógica da IA ClarinhaBubi
def clarinha_operar():
    simbolo = 'BTCUSDT'
    quantidade = 0.001
    try:
        ticker = client.get_ticker(symbol=simbolo)
        preco = float(ticker['lastPrice'])
        ordem = client.futures_create_order(
            symbol=simbolo,
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=quantidade
        )
        texto = f"🟢 Compra Executada: {quantidade} {simbolo} a {preco:.2f} USDT"
        print(texto)
        ordens_executadas.insert(0, texto)
    except Exception as e:
        erro = f"Erro: {str(e)}"
        print(erro)
        ordens_executadas.insert(0, erro)

# Rota manual
@app.route('/executar', methods=['POST'])
def executar_ordem():
    clarinha_operar()
    return '', 204

# Rota automática
@app.route('/automatica', methods=['POST'])
def modo_automatico():
    def loop():
        while True:
            clarinha_operar()
            time.sleep(120)  # Executa a cada 2 minutos
    threading.Thread(target=loop).start()
    return '', 204

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)