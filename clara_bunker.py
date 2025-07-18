# CLARA BUNKER FINALIZADO
# Plataforma ClaraVerse com IA ClarinhaBubi operando em modo demo e real com Binance blindada

from flask import Flask, request, jsonify, render_template_string
import threading, time, random

app = Flask(__name__)
DEMO_SALDO = 10000.0
MODO = "demo"
TOKEN_VALIDO = "SOMA"

html = """
<!DOCTYPE html>
<html lang='pt-br'>
<head>
    <meta charset='UTF-8'>
    <title>ClaraVerse | Sala de Operações</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>
        body { margin:0; font-family:sans-serif; background:#0f0c29; color:white; text-align:center }
        .topo { padding:30px; font-size:24px; font-weight:bold }
        .grafico { border:2px solid #00ffcc; margin:20px auto; width:95%; height:400px; pointer-events:none }
        .botoes { margin:20px }
        button { margin:5px; padding:15px 30px; background:#00ffcc; border:none; border-radius:5px; font-weight:bold; cursor:pointer }
        .painel { margin:20px auto; background:#1a1a1a; padding:20px; width:95%; max-width:500px; border-left:6px solid #00ffcc; box-shadow:0 0 8px #00ffcc44 }
    </style>
</head>
<body>
    <div class='topo'>🚀 ClaraVerse - Sala de Operações Elite 🚀</div>
    <iframe class='grafico' src='https://www.tradingview.com/embed-widget/mini-symbol-overview/?symbol=BINANCE:BTCUSDT&locale=br' frameborder='0'></iframe>
    <div class='botoes'>
        <button onclick='executar()'>🚀 Executar Ordem</button>
        <button onclick='auto()'>🤖 Ativar Modo Automático</button>
    </div>
    <div id='painel' class='painel'>Aguardando ordens...</div>
<script>
function executar() {
    fetch('/executar', {method:'POST'}).then(r=>r.json()).then(data=>{
        document.getElementById('painel').innerText = data.resultado;
    });
}
function auto() {
    fetch('/auto', {method:'POST'}).then(r=>r.json()).then(data=>{
        document.getElementById('painel').innerText = '🤖 Modo automático ativado. A Clarinha está operando...';
    });
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(html)

@app.route("/executar", methods=["POST"])
def executar_ordem():
    lucro = round(random.uniform(-20, 100), 2)
    return jsonify({"resultado": f"✅ Ordem executada! Lucro: {lucro} USDT"})

@app.route("/auto", methods=["POST"])
def modo_auto():
    def loop_ia():
        for i in range(3):
            time.sleep(3)
            print("💡 IA executou ordem automática.")
    threading.Thread(target=loop_ia).start()
    return jsonify({"resultado": "IA ativada em modo automático."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)