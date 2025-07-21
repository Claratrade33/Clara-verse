import os
from flask import Flask, request, jsonify, render_template_string
from binance.client import Client
import openai
from cryptography.fernet import Fernet

# CHAVE FERNET
FERNET_KEY = "ylh-urjGFbF60dGJcGjEWY5SKGbhui-8SUItRz7YMZk="
fernet = Fernet(FERNET_KEY.encode())

# CHAVES CRIPTOGRAFADAS
API_KEY = fernet.decrypt(b"gAAAAABoe_tmC3u_LkLDxTnp5p-7wgMiHVcKvJIOgEQFfBTWjRx5CC2Ts3Z1PPx-vEA1ChEFZMxi1THdulmp8WK8wCJzBmS8vHAWEU4pooCBt8tVrlf0NkfOur-pEtjpjZt6NSpPUbhFvIqjtwNDnQAtMQL_mPfM8Dype0oShNoTkcMnECOsmF0=").decode()
API_SECRET = fernet.decrypt(b"gAAAAABoe_tmrN2tKPQsPVYlnxp-wKItqZNirJXN_9eKHhle-_z_eud6i1pGpdG-ZRsDf_g26q2jlRixSXv8h_ZwOv5p4lu3AshCRbHXRpPvcHJ8LaoqGOP2ZQNH4h-8WUdPOSlEXYz2NXJHOlYMigWiyZO8d2w0NYlQa0N2Vv-CpDMOXuIXcN8=").decode()
OPENAI_KEY = fernet.decrypt(b"gAAAAABoe_xqx7jAACfbXHrmoFSrEU_x2uJbVsrYNvjpn-IWOD02jHr6pAtSznZZkFd0cE50OcdsFukYMR441vQgThN8UaoeQXvbD76jS3wJkvlcGJcwfbwWOi2dEd9MgZuEULE92B9UYLFVzgKzP3ZJ-IRmsF_ppg==").decode()

# CLIENTES
binance = Client(API_KEY, API_SECRET)
openai.api_key = OPENAI_KEY
app = Flask(__name__)

# HTML EMBUTIDO
html = """
<!DOCTYPE html>
<html>
<head>
  <title>Clara Bunker</title>
  <script src="https://s3.tradingview.com/tv.js"></script>
</head>
<body>
  <h1>Clara Bunker - Operações Automatizadas</h1>
  <div id="tv_chart_container"></div>
  <script>
    new TradingView.widget({
      "container_id": "tv_chart_container",
      "width": "100%",
      "height": 400,
      "symbol": "BINANCE:BTCUSDT",
      "interval": "5",
      "timezone": "Etc/UTC",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "hide_side_toolbar": false,
      "allow_symbol_change": true,
      "studies": []
    });
  </script>
  <form method="post" action="/auto">
    <button type="submit">AUTOMÁTICO</button>
  </form>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(html)

@app.route("/auto", methods=["POST"])
def auto_trade():
    msg = "Clara, analise os pares BTC/USDT, SUI/USDT e PEPE/USDT e diga: entrada, alvo, stop e confiança."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": msg}]
    )
    result = response.choices[0].message.content

    # Lógica para enviar ordens reais para Binance
    print("GPT respondeu:", result)
    return f"<h2>Resultado da Clara:</h2><pre>{result}</pre><a href='/'>Voltar</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)