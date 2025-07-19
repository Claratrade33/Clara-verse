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

# INTERFACE HTML ESTILO CORRETORA MODERNA
html = '''
<!DOCTYPE html>
<html>
<head>
    <title>ClaraVerse - Operações</title>
    <style>
        body {
            margin: 0; padding: 0; background-color: #0f0f0f; font-family: 'Segoe UI', sans-serif; color: #eee;
        }
        header {
            background-color: #111; padding: 20px; text-align: center; border-bottom: 1px solid #00ffc8;
        }
        header h1 {
            margin: 0; font-size: 26px; color: #00ffc8;
        }
        .container {
            max-width: 600px; margin: 40px auto; text-align: center;
        }
        select, button {
            padding: 14px; font-size: 16px; margin: 10px 0; border-radius: 6px; border: none;
        }
        select {
            width: 100%; background: #1e1e1e; color: #fff;
        }
        button {
            background-color: #00ffc8; color: #000; cursor: pointer;
            transition: background 0.3s ease;
        }
        button:hover {
            background-color: #00cfa6;
        }
        #result {
            background: #1e1e1e; padding: 20px; margin-top: 20px;
            border: 1px solid #00ffc8; border-radius: 8px; font-size: 18px; white-space: pre-line;
        }
    </style>
</head>
<body>
    <header>
        <h1>🧠 ClaraVerse - Sala de Operações</h1>
    </header>
    <div class="container">
        <p>Escolha o par e clique em <strong>AUTOMÁTICO</strong>:</p>
        <select id="symbol">
            <option value="PEPEUSDT">PEPE/USDT</option>
            <option value="SUIUSDT">SUI/USDT</option>
        </select><br>
        <button onclick="enviar()">🚀 AUTOMÁTICO</button>
        <div id="result"></div>
    </div>
    <script>
        function enviar() {
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
    atual = closes[-1]
    contexto = f"Últimos fechamentos de {symbol}: {closes}\nRetorne uma análise de trading com entrada, alvo, stop e confiança."
    resposta = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Você é uma IA trader especialista."},
                  {"role": "user", "content": contexto}],
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
