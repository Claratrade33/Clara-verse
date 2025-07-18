# CLARA BUNKER FINAL 💎
# ClaraVerse com IA ClarinhaBubi operando em modo demo com painel de corretora real

from flask import Flask, render_template_string, request, jsonify
import threading
import time
import random

app = Flask(__name__)

# ==== CONFIGURAÇÕES DE SISTEMA ====
DEMO_SALDO = 10000.0
MODO = "demo"
TOKEN_VALIDO = "SOMA"

# ==== HTML INTEGRADO ====
html_bunker = '''
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
      padding: 30px 0; font-size: 28px; font-weight: bold; text-align: center;
    }
    .painel {
      display: flex; flex-direction: column; align-items: center;
    }
    iframe {
      border: 3px solid #00ffcc; border-radius: 8px;
      width: 90%; max-width: 900px; height: 400px;
      pointer-events: none;
      margin-bottom: 20px;
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
  <div class="topo">🚀 ClaraVerse - Sala de Operações Elite com ClarinhaBubi 🚀</div>
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

# ==== ROTAS ====
@app.route("/")
def index():
    return render_template_string(html_bunker)

@app.route("/executar", methods=["POST"])
def executar():
    lucro = round(random.uniform(-10, 40), 2)
    return jsonify({"resultado": f"Lucro simulado: {lucro} USDT"})

@app.route("/auto", methods=["POST"])
def auto():
    def rotina_auto():
        for _ in range(3):
            time.sleep(2)
            print("💡 ClarinhaBubi executou ordem automática.")
    threading.Thread(target=rotina_auto).start()
    return jsonify({"resultado": "Modo automático ativado."})

# ==== INICIAR ====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)