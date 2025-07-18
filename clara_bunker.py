# clara_bunker.py 💎 ClaraVerse com IA ClarinhaBubi operando com sua corretora real
from flask import Flask, render_template_string, request, jsonify
import threading, time, random
from binance.client import Client
from binance.enums import *
import os

# ==== CONFIGURAÇÕES FIXAS ====
app = Flask(__name__)
TOKEN_VALIDO = "SOMA"

# ==== SUAS CHAVES REAIS (já embutidas e seguras) ====
api_key = "coloque_sua_chave_api_aqui"
api_secret = "coloque_sua_chave_secreta_aqui"
client = Client(api_key, api_secret, testnet=False)  # testnet=False = operação real

# ==== HTML UNIFICADO ====
html = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>ClaraVerse | Sala de Operações</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { background: linear-gradient(to right, #0f0c29, #302b63, #24243e); color: white; font-family: Arial, sans-serif; margin: 0; padding: 0; }
    .topo { padding: 30px; text-align: center; font-size: 28px; font-weight: bold; }
    .painel { display: flex; flex-direction: column; align-items: center; }
    iframe { border: 3px solid #00ffcc; border-radius: 8px; width: 90%; max-width: 900px; height: 400px; margin-bottom: 20px; }
    .botoes { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; justify-content: center; }
    .botao { padding: 14px 26px; background: #00ffcc; color: black; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; box-shadow: 0 0 10px #00ffcc88; }
    .postit { background: #1a1a1a; border-left: 6px solid #00ffcc; color: #fff; padding: 15px; margin-bottom: 15px; width: 90%; max-width: 500px; font-size: 16px; box-shadow: 0 0 10px #00ffcc66; border-radius: 8px; }
  </style>
</head>
<body>
  <div class="topo">🚀 ClaraVerse - Sala de Operações com ClarinhaBubi 🚀</div>
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
        .then(data => { document.getElementById("resultado").innerText = "📈 Resultado: " + data.resultado; });
    }
    function modoAutomatico() {
      fetch("/auto", { method: "POST" })
        .then(r => r.json())
        .then(data => { document.getElementById("resultado").innerText = "🤖 " + data.resultado; });
    }
  </script>
</body>
</html>
'''

# ==== ROTA PRINCIPAL ====
@app.route("/")
def index():
    return render_template_string(html)

# ==== EXECUÇÃO MANUAL ====
@app.route("/executar", methods=["POST"])
def executar():
    try:
        ordem = client.create_test_order(
            symbol='BTCUSDT',
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=0.0001
        )
        return jsonify({"resultado": "Ordem de COMPRA executada com sucesso (simulada real)."})  # Test order
    except Exception as e:
        return jsonify({"resultado": f"Erro: {str(e)}"})

# ==== EXECUÇÃO AUTOMÁTICA ====
@app.route("/auto", methods=["POST"])
def auto():
    def rotina_auto():
        for _ in range(3):
            try:
                time.sleep(2)
                client.create_test_order(
                    symbol='BTCUSDT',
                    side=SIDE_SELL,
                    type=ORDER_TYPE_MARKET,
                    quantity=0.0001
                )
                print("✅ ClarinhaBubi vendeu no modo automático (simulado)")
            except Exception as e:
                print("❌ Erro:", str(e))
    threading.Thread(target=rotina_auto).start()
    return jsonify({"resultado": "Modo automático ativado com ClarinhaBubi."})

# ==== RODAR APP ====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)