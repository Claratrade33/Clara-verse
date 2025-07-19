import os
from flask import Flask, request, jsonify, render_template_string
from binance.client import Client
from openai import OpenAI
from cryptography.fernet import Fernet

# ==== CHAVE FERNET ====
FERNET_KEY = "ylh-urjGFb60dGJcGjEWY5SKGbhui-8SUItRz7YMZk="
fernet = Fernet(FERNET_KEY.encode())

# ==== CHAVES CRIPTOGRAFADAS ====
API_KEY = fernet.decrypt(b"gAAAAABoe_tmC3u_LkLDxTnp5p-7wgMiHVckvJIOgEQFfBTWjRx5CC2Ts3Z1PPx-vEA1ChEFZMxi1THdulmp8WK8wCJzBmS8vHAWEU4pooCBt8tVrlf0NkfOur-pEtjpJZt6NSpPUbhFvIqjtwNDnQAtMQL_mPfM8Dype0oShNoTkcMnECOsmF0=").decode()
API_SECRET = fernet.decrypt(b"gAAAAABoe_tmrN2tKPQsPVYlnxp-wKItqZNirJXN_9eKHhle-_z_eud6i1pGpdG-ZRsDf_g26q2jlRixSXv8h_ZwOv5p4lu3AshCRbHXRpPvcHJ8LaoqGOP2ZQNH4h-8WUdPOS1EXYzZNXJHOLYMigWiyZO8d2w0NY1Qa0N2Vv-CpDMOXuIXcN8=").decode()
OPENAI_KEY = fernet.decrypt(b"gAAAAABoe_xqx7jAACfbXHKxzF7XpmppgfkAYeX0fEHoOCfXz_lFxtzxnQqzty3LV1xFYvX9JllSyCd-jWnbn9acqFoMf4fGhA==").decode()

# ==== INICIALIZAÇÃO ====
app = Flask(__name__)
binance = Client(API_KEY, API_SECRET)
client_openai = OpenAI(api_key=OPENAI_KEY)

# ==== HTML INTERFACE ====
html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Clara Bunker</title>
</head>
<body>
    <h1>Bem-vindo à Sala de Operações Clara</h1>
    <form action="/operar" method="post">
        <label>Moeda (ex: BTCUSDT):</label><br>
        <input type="text" name="par" value="BTCUSDT"><br><br>
        <button type="submit">ENTRAR</button>
    </form>
</body>
</html>
'''

# ==== ROTA PRINCIPAL ====
@app.route('/')
def index():
    return render_template_string(html)

# ==== LÓGICA DE OPERAÇÃO ====
@app.route('/operar', methods=['POST'])
def operar():
    par = request.form.get('par', 'BTCUSDT')

    try:
        candles = binance.get_klines(symbol=par, interval=Client.KLINE_INTERVAL_1MINUTE, limit=10)
        prices = [float(c[4]) for c in candles]
        media = sum(prices) / len(prices)

        # Consulta à OpenAI
        prompt = f"Últimos preços: {prices}. Média: {media:.2f}. Você recomendaria entrar comprado ou vendido?"
        response = client_openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        decisao = response.choices[0].message.content.strip()
        return jsonify({
            "par": par,
            "preco_atual": prices[-1],
            "media": media,
            "decisao": decisao
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ==== PARA RODAR LOCALMENTE ====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
