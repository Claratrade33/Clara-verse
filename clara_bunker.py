import os
from flask import Flask, render_template_string, request, jsonify
from cryptography.fernet import Fernet
from binance.client import Client
from openai import OpenAI

# CHAVE FERNET
FERNET_KEY = "WS2w38PfSNFIwUDWHEZSUVaaBbC36rY0AWd_9Url870="
fernet = Fernet(FERNET_KEY.encode())

# CHAVES CRIPTOGRAFADAS (Binance e OpenAI)
API_KEY = fernet.decrypt(b"gAAAAABofByBegKeqcSRN-lmgaanOOcM5O0Dtu7z2iYK_-suiNcRNlSiFdeInAvys66mWh1NBoiQNmqUwqZ_T-6H4e6rN5ZQRUmWuN_uhl5jb7ZfVrqVjAxXuaVSv9AMclZouDtigmvkQSLS58SSIVNhLjpjdmtX6xL9BN71bo1lsOltx5rUq8I=").decode()
API_SECRET = fernet.decrypt(b"gAAAAABofByB-BP_jDBCmDRIm5yL397B-p0w14TW8ElNTV5KAMXDY3Bd3p-Gw0N5TgwJ4wlF7URd7t1KnexICFpNX5fI9M6mfyrsCm4z1A3uDFO7DBkDdW5cR795ZDNp3tKRiQO_EE2-Xj7r-OONhYXXVHWKsaS_jOjmZR3iOtqFqzn-dEJc2I0=").decode()
OPENAI_KEY = fernet.decrypt(b"gAAAAABofcqTHnBgOXfjUuN5WYFAqWfUZLMVoqLqPGhWWvMKPzIDHe8raM1n2Jz9moY8uwvq4mvNHsv-jmGWqAoJAC_8W1OHWAVk9T1Et64EbbYCG6xAI_XURJAKslk2X6cwR3pNiEr0WZq7Ax3AZqxFOf3Z5M2HhOw==").decode()

# INICIALIZAÇÃO
app = Flask(__name__)
binance = Client(API_KEY, API_SECRET)
client_openai = OpenAI(api_key=OPENAI_KEY)

# HTML EMBUTIDO COM VISUAL DE CORRETORA
html = '''
<!DOCTYPE html>
<html>
<head>
    <title>ClaraVerse - Sala de Operações</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #0d1117;
            color: #c9d1d9;
            margin: 0;
            padding: 20px;
            text-align: center;
        }
        h1 {
            color: #58a6ff;
            margin-bottom: 10px;
        }
        select, button {
            font-size: 16px;
            padding: 12px;
            margin: 10px;
            border: none;
            border-radius: 5px;
        }
        select {
            background-color: #161b22;
            color: #c9d1d9;
        }
        button {
            background-color: #238636;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #2ea043;
        }
        #result {
            margin-top: 30px;
            font-size: 18px;
            white-space: pre-line;
            background: #161b22;
            padding: 20px;
            border-radius: 10px;
            display: inline-block;
            text-align: left;
        }
    </style>
</head>
<body>
    <h1>📊 ClaraVerse - Sala de Operações</h1>
    <p>Escolha o par desejado e clique em <b>AUTOMÁTICO</b>:</p>
    <select id="symbol">
        <option value="BTCUSDT">BTC/USDT</option>
        <option value="ETHUSDT">ETH/USDT</option>
        <option value="SUIUSDT">SUI/USDT</option>
        <option value="PEPEUSDT">PEPE/USDT</option>
    </select><br>
    <button onclick="enviar()">🚀 AUTOMÁTICO</button>
    <div id="result"></div>

    <script>
        function enviar() {
            const symbol = document.getElementById('symbol').value;
            document.getElementById('result').innerText = '⏳ Analisando...';
            fetch('/analise', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ symbol: symbol })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('result').innerText =
                    "🎯 ENTRADA: " + data.entrada + "\\n" +
                    "🛑 STOP: " + data.stop + "\\n" +
                    "🎯 ALVO: " + data.alvo + "\\n" +
                    "📊 CONFIANÇA: " + data.confianca;
            })
            .catch(err => {
                document.getElementById('result').innerText = "Erro ao obter análise.";
            });
        }
    </script>
</body>
</html>
'''

# ROTAS FLASK
@app.route('/')
def index():
    return render_template_string(html)

@app.route('/analise', methods=['POST'])
def analise():
    data = request.get_json()
    symbol = data['symbol']
    candles = binance.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE, limit=100)
    closes = [float(c[4]) for c in candles]
    atual = closes[-1]
    contexto = f"Últimos fechamentos de {symbol}: {closes}\nRetorne uma análise de trading com entrada, alvo, stop e confiança."

    resposta = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é uma IA trader especialista em criptomoedas."},
            {"role": "user", "content": contexto}
        ],
        temperature=0.3
    )
    texto = resposta.choices[0].message.content

    partes = {k: '' for k in ['entrada', 'stop', 'alvo', 'confianca']}
    for linha in texto.lower().splitlines():
        for chave in partes:
            if chave in linha:
                partes[chave] = ''.join(c for c in linha if c.isdigit() or c in ',.')

    return jsonify(partes)

# PARA RENDER
application = app
