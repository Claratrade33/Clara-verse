from flask import Flask, render_template_string, request, jsonify
from cryptography.fernet import Fernet
import threading
import random
import time

app = Flask(__name__)

# === CHAVES TESTNET GERADAS E CRIPTOGRAFADAS ===
fernet_key = b'0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA='
fernet = Fernet(fernet_key)

api_key_cript = b'gAAAAABmY4e_p1Z_gQhCq5aTFOI3lp3n8xHxaUGemGo2A0ZdbuW9Xz7JyzjR9guMPu2EkzXxx64b6X3dHfO-3Qh09C2H81B6hA=='
api_secret_cript = b'gAAAAABmY4e_YxxnQGek9RfXYDoGrAGV6iEMtHti6KhBvTttMJ8Y8w1vU7M7qzELZdApFNU6MAq4p0tbiqI07oKQTXfSLuOCSg=='

api_key = fernet.decrypt(api_key_cript).decode()
api_secret = fernet.decrypt(api_secret_cript).decode()

# === VARIÁVEIS DE CONTROLE ===
demo_saldo = 10000.0
modo = "demo"
token_valido = "SOMA"
historico = []

# === HTML FRONT ===
html = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>ClaraVerse | Sala de Operações</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      margin: 0; font-family: 'Segoe UI', sans-serif;
      background: linear-gradient(to right, #0f0c29, #302b63, #24243e);
      color: white;
    }
    .topo {
      padding: 30px; font-size: 28px; font-weight: bold; text-align: center;
    }
    .painel {
      display: flex; flex-direction: column; align-items: center;
    }
    iframe {
      border: 3px solid #00ffcc; border-radius: 8px;
      width: 90%; max-width: 900px; height: 400px;
      pointer-events: none; margin-bottom: 20px;
    }
    .botoes {
      display: flex; flex-wrap: wrap; justify-content: center;
      gap: 10px; margin-bottom: 20px;
    }
    .botao {
      padding: 14px 26px;
      background: #00ffcc;
      color: #000; font-weight: bold;
      border: none; border-radius: 6px;
      cursor: pointer;
      box-shadow: 0 0 10px #00ffcc88;
    }
    .postit {
      background: #1a1a1a;
      border-left: 6px solid #00ffcc;
      color: #fff;
      padding: 15px;
      margin-bottom: 15px;
      width: 90%; max-width: 500px;
      font-size: 16px;
      box-shadow: 0 0 10px #00ffcc66;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <div class="topo">🚀 ClaraVerse - Sala de Operações com ClarinhaBubi</div>
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
          document.getElementById("resultado").innerText = "🤖 Modo automático ativado com ClarinhaBubi!";
        });
    }
  </script>
</body>
</html>
'''

# === ROTAS FLASK ===
@app.route("/")
def index():
    return render_template_string(html)

@app.route("/executar", methods=["POST"])
def executar_ordem():
    global demo_saldo
    lucro = round(random.uniform(-20, 45), 2)
    demo_saldo += lucro
    resultado = f"💰 Lucro: {lucro} USDT | Saldo Atual: {round(demo_saldo,2)} USDT"
    historico.append(resultado)
    return jsonify({"resultado": resultado})

@app.route("/auto", methods=["POST"])
def modo_auto():
    def operacao_auto():
        global demo_saldo
        for _ in range(3):
            time.sleep(2)
            lucro = round(random.uniform(-15, 60), 2)
            demo_saldo += lucro
            print(f"🤖 ClarinhaBubi executou: +{lucro} USDT")
    threading.Thread(target=operacao_auto).start()
    return jsonify({"resultado": "Modo automático ativado com IA ClarinhaBubi"})

# === RODAR APP ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)