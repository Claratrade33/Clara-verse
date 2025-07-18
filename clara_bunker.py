# CLARA BUNKER UNIFICADO
# Plataforma ClaraVerse com IA ClarinhaBubi operando em modo demo/real com Binance

from flask import Flask, render_template_string, request, jsonify
import threading
import time
import random

# ====== CONFIGURAÇÕES INICIAIS ======
app = Flask(__name__)
DEMO_SALDO = 10000.0
MODO = "demo"
TOKEN_VALIDO = "SOMA"

# ====== INTERFACE FUTURISTA HTML ======
html_base = '''
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
            color: white; text-align: center;
        }
        .topo { padding: 30px 0; font-size: 24px; font-weight: bold; }
        .grafico-container { border: 3px solid #00ffcc; margin: 20px auto; width: 90%; max-width: 900px; height: 400px; pointer-events: none; }
        .botao { margin: 10px; padding: 15px 30px; background: #00ffcc; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .postit { background: #1a1a1a; border-left: 6px solid #00ffcc; margin: 20px auto; padding: 20px; width: 90%; max-width: 400px; text-align: left; box-shadow: 0 0 10px #00ffcc66; }
    </style>
</head>
<body>
    <div class="topo">🚀 ClaraVerse - Sala de Operações Elite 🚀</div>
    <iframe class="grafico-container" src="https://www.tradingview.com/embed-widget/mini-symbol-overview/?symbol=BINANCE:BTCUSDT&locale=br" frameborder="0"></iframe>
    <div>
        <button class="botao" onclick="executarOrdem()">Executar Ordem</button>
        <button class="botao" onclick="modoAutomatico()">Modo Automático</button>
    </div>
    <div id="resultado" class="postit">🔍 Resultados aparecerão aqui após execução.</div>
<script>
function executarOrdem() {
    fetch("/executar", {method: "POST"})
    .then(r => r.json())
    .then(data => {
        document.getElementById("resultado").innerText = "📈 Resultado: " + data.resultado;
    });
}
function modoAutomatico() {
    fetch("/auto", {method: "POST"})
    .then(r => r.json())
    .then(data => {
        document.getElementById("resultado").innerText = "🤖 Modo automático iniciado!";
    });
}
</script>
</body>
</html>
'''

# ====== ROTAS ======
@app.route("/")
def index():
    return render_template_string(html_base)

@app.route("/executar", methods=["POST"])
def executar():
    lucro = round(random.uniform(-15, 75), 2)
    return jsonify({"resultado": f"Lucro obtido: {lucro} USDT"})

@app.route("/auto", methods=["POST"])
def auto():
    def rotina_auto():
        for _ in range(3):
            time.sleep(3)
            print("IA executou ordem automática.")
    threading.Thread(target=rotina_auto).start()
    return jsonify({"resultado": "Modo automático ativado."})

# ====== INICIALIZAÇÃO ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
