import os
from flask import Flask, render_template_string, request, jsonify
from cryptography.fernet import Fernet
from binance.client import Client
from openai import OpenAI

# CHAVE FERNET USADA PARA DESCRIPTOGRAFAR
FERNET_KEY = "WS2w38PfSNFIwUDWHEZSUVaaBbC36rY0AWd_9Url870="
fernet = Fernet(FERNET_KEY.encode())

# CHAVES CRIPTOGRAFADAS
API_KEY = fernet.decrypt(b"gAAAAABofByBegKeqcSRN-lmgaanOOcM5O0Dtu7z2iYK_-suiNcRNlSiFdeInAvys66mWh1NBoiQNmqUwqZ_T-6H4e6rN5ZQRUmWuN_uhl5jb7ZfVrqVjAxXuaVSv9AMclZouDtigmvkQSLS58SSIVNhLjpjdmtX6xL9BN71bo1lsOltx5rUq8I=").decode()
API_SECRET = fernet.decrypt(b"gAAAAABofByB-BP_jDBCmDRIm5yL397B-p0w14TW8ElNTV5KAMXDY3Bd3p-Gw0N5TgwJ4wlF7URd7t1KnexICFpNX5fI9M6mfyrsCm4z1A3uDFO7DBkDdW5cR795ZDNp3tKRiQO_EE2-Xj7r-OONhYXXVHWKsaS_jOjmZR3iOtqFqzn-dEJc2I0=").decode()
OPENAI_KEY = fernet.decrypt(b"gAAAAABofByBbLcXkUQfo6P0jLJP93NXWM_kSaV-0P1UIhpxZ05I719DGuTUPHM6sFdeAFimCoSBU2RGTN8nyteMd9o3V8gZ7w==").decode()

# INICIALIZAÇÃO
app = Flask(__name__)
binance = Client(API_KEY, API_SECRET)
client_openai = OpenAI(api_key=OPENAI_KEY)

# INTERFACE VISUAL ATUALIZADA
html = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ClaraVerse | Painel de Operações</title>
    <style>
        body {
            margin: 0; padding: 0;
            font-family: Arial, sans-serif;
            background-color: #0f0f0f;
            color: #fff;
        }
        header {
            background: #00ffcc;
            color: #000;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }
        .painel {
            padding: 40px 20px;
            max-width: 600px;
            margin: auto;
            background: #1e1e1e;
            border-radius: 10px;
            box-shadow: 0 0 15px #00ffcc33;
        }
        select, button {
            padding: 15px;
            font-size: 16px;
            margin-top: 15px;
            border: none;
            border-radius: 5px;
        }
        select {
            width: 100%;
            background-color: #fff;
            color: #000;
        }
        button {
            background-color: #00ffcc;
            color: #000;
            width: 100%;
            font-weight: bold;
        }
        #result {
            margin-top: 25px;
            font-size: 18px;
            background: #121212;
            padding: 20px;
            border-radius: 10px;
            white-space: pre-line;
        }
    </style>
</head>
<body>
    <header>🧠 ClaraVerse - Painel de Operações</header>
    <div class="painel">
        <label for="symbol">Escolha o par:</label>
        <select id="symbol">
            <option value="PEPEUSDT">PEPE/USDT</option>
            <option value="SUIUSDT">SUI/USDT</option>
            <option value="BTCUSDT">BTC/USDT</option>
            <option value="ETHUSDT">ETH/USDT</option>
        </select>
        <button onclick="enviar()">📈 Analisar AUTOMATICAMENTE</button>
        <div id="result">⏳ Aguardando análise...</div>
    </div>
    <script>
        function enviar() {
            document.getElementById('result').innerText = "🔍 Gerando análise...";
            const symbol = document.getElementById('symbol').value;
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
                document.getElementById('result').innerText = "❌ Erro ao buscar análise.";
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html)

@app.route('/analise', methods=['POST'])
def analise():
    data = request.get_json()
    symbol = data['symbol']
    candles = binance.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE, limit=100)
    closes = [float(c[4]) for c in candles]
    contexto = f"Últimos fechamentos de {symbol}: {closes}\nRetorne uma análise de trading com entrada, alvo, stop e confiança."
    resposta = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é uma IA trader especialista."},
            {"role": "user", "content": contexto}
        ],
        temperature=0.3
    )
    texto = resposta.choices[0].message.content
    partes = {k: '' for k in ['entrada', 'stop', 'alvo', 'confianca']}
    for linha in texto.splitlines():
        for chave in partes:
            if chave in linha.lower():
                partes[chave] = ''.join(c for c in linha if c.isdigit() or c in ',.')
    return jsonify(partes)

# PARA RENDER
application = app
