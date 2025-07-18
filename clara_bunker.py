# CLARA BUNKER FINAL 💎
# ClaraVerse com IA ClarinhaBubi operando com chaves reais protegidas

from flask import Flask, render_template_string, request, jsonify
from cryptography.fernet import Fernet
from binance.client import Client
import threading
import time
import random
import os

app = Flask(__name__)

# ==== SEGURANÇA ====
chave_fernet = Fernet(b"0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA=")

# Suas chaves protegidas (fornecidas por você, criptografadas)
api_key_criptografada = b"gAAAAABmW9wqzF3svvmr3-4SnVAgcrqDF7jM5F20W77MzY8V1pLiih6eSLEr8GHNbWeV9F9H5IQdvrlq9sl0AP6KkY7y9TA8Sp_4t68d7ytTfU2tk9zXiZzLGAlI4z_vvqnDhOlDWf1g"
api_secret_criptografada = b"gAAAAABmW9wr8WlcvwHFKG2QeCKyhnx3qABDF7jlC7BFUtbwEHG-F1F20XxyimmlDdL5RW0TleqsvEV_zsPL9dImBRS5atVvIC-DmRZUPdOPgyKM4ZULBcs="

api_key = chave_fernet.decrypt(api_key_criptografada).decode()
api_secret = chave_fernet.decrypt(api_secret_criptografada).decode()

cliente = Client(api_key, api_secret, testnet=False)

# ==== HTML INTEGRADO ====
html = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>ClaraVerse | Sala de Operações Real</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { margin: 0; font-family: 'Segoe UI', sans-serif;
      background: linear-gradient(to right, #0f0c29, #302b63, #24243e);
      color: white; }
    .topo { padding: 30px 0; font-size: 28px; font-weight: bold; text-align: center; }
    .painel { display: flex; flex-direction: column; align-items: center; }
    iframe { border: 3px solid #00ffcc; border-radius: 8px;
      width: 90%; max-width: 900px; height: 400px;
      pointer-events: none; margin-bottom: 20px; }
    .botoes { display: flex; flex-wrap: wrap; justify-content: center;
      gap: 10px; margin-bottom: 20px; }
    .botao { padding: 14px 26px;
      background: #00ffcc; color: #000; font-weight: bold;
      border: none; border-radius: 6px; cursor: pointer;
      box-shadow: 0 0 10px #00ffcc88; }
    .postit { background: #1a1a1a; border-left: 6px solid #00ffcc;
      color: #fff; padding: 15px; margin-bottom: 15px;
      width: 90%; max-width: 500px; font-size: 16px;
      box-shadow: 0 0 10px #00ffcc66; border-radius: 8px; }
  </style>
</head>
<body>
  <div class="topo">🚀 ClaraVerse - Sala de Operações Real com ClarinhaBubi 🚀</div>
  <div class="painel">
    <iframe src="https://www.tradingview.com/embed-widget/mini-symbol-overview/?symbol=BINANCE:BTCUSDT&locale=br"></iframe>

    <div class="botoes">
      <button class="botao" onclick="executarOrdem()">Executar Ordem</button>
      <button class="botao" onclick="modoAutomatico()">Modo Automático</button>
    </div>

    <div id="resultado" class="postit">🔍 Resultados aparecerão aqui após execução.</div>
  </div>

  <script>
    function executarOrdem() {
      fetch("/executar", { method: "POST" })
        .then(r => r.json())
        .then(data => {
          document.getElementById("resultado").innerText = "📈 Resultado: " + data.resultado;
        });
    }

    function modoAutomatico() {
      fetch("/auto", { method: "POST" })
        .then(r => r.json())
        .then(data => {
          document.getElementById("resultado").innerText = "🤖 " + data.resultado;
        });
    }
  </script>
</body>
</html>
'''

# ==== ROTAS ====
@app.route("/")
def index():
    return render_template_string(html)

@app.route("/executar", methods=["POST"])
def executar():
    try:
        ordem = cliente.futures_create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            quantity=0.001
        )
        preco = ordem['fills'][0]['price']
        return jsonify({"resultado": f"Ordem executada com sucesso! Preço: {preco}"})
    except Exception as e:
        return jsonify({"resultado": f"Erro ao executar: {e}"})


@app.route("/auto", methods=["POST"])
def auto():
    def loop_auto():
        for _ in range(3):
            try:
                cliente.futures_create_order(
                    symbol="BTCUSDT",
                    side="BUY",
                    type="MARKET",
                    quantity=0.001
                )
                print("✅ Ordem automática executada.")
            except Exception as e:
                print("Erro:", e)
            time.sleep(3)

    threading.Thread(target=loop_auto).start()
    return jsonify({"resultado": "Modo automático iniciado com IA ClarinhaBubi."})


# ==== INICIAR ====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)