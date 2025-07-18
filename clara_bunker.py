# CLARA BUNKER UNIFICADO
# Plataforma ClaraVerse com IA ClarinhaBubi operando em modo demo/real com Binance

from flask import Flask, render_template_string, request, jsonify, redirect, url_for
import threading
import time
import random

app = Flask(__name__)
DEMO_SALDO = 10000.0
MODO = "demo"
TOKEN_VALIDO = "SOMA"
ULTIMO_RESULTADO = "🔍 Resultados aparecerão aqui após execução."

# ====== HTML FACHADA ======
html_fachada = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ClaraVerse - Embarque</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            background: linear-gradient(to right, #0f0c29, #302b63, #24243e);
            color: white; text-align: center;
            font-family: 'Segoe UI', sans-serif;
            padding: 50px;
        }
        input, button {
            padding: 14px; font-size: 16px; margin-top: 15px;
            border-radius: 8px; border: none;
        }
        input {
            width: 240px;
        }
        button {
            background: #00ffcc; color: black; font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>🚀 Bem-vindo à ClaraVerse</h1>
    <p>Insira seu token de acesso para embarcar:</p>
    <form method="POST">
        <input type="text" name="token" placeholder="Digite o token">
        <br>
        <button type="submit">EMBARCAR NA NAVE</button>
    </form>
</body>
</html>
'''

# ====== HTML SALA DE OPERAÇÕES ======
html_sala = '''
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
    <div id="resultado" class="postit">{{resultado}}</div>
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
        document.getElementById("resultado").innerText = "🤖 " + data.resultado;
    });
}
</script>
</body>
</html>
'''

# ====== ROTAS ======

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        token = request.form.get("token", "").strip().upper()
        if token == TOKEN_VALIDO:
            return redirect(url_for("sala_operacoes"))
    return render_template_string(html_fachada)

@app.route("/sala")
def sala_operacoes():
    return render_template_string(html_sala, resultado=ULTIMO_RESULTADO)

@app.route("/executar", methods=["POST"])
def executar():
    global ULTIMO_RESULTADO
    lucro = round(random.uniform(-15, 75), 2)
    ULTIMO_RESULTADO = f"Lucro obtido: {lucro} USDT"
    return jsonify({"resultado": ULTIMO_RESULTADO})

@app.route("/auto", methods=["POST"])
def auto():
    def rotina_auto():
        global ULTIMO_RESULTADO
        for _ in range(3):
            time.sleep(2)
            roi = round(random.uniform(-5, 7), 2)
            ULTIMO_RESULTADO = f"IA executou com ROI de {roi}%"
    threading.Thread(target=rotina_auto).start()
    return jsonify({"resultado": "Modo automático ativado."})

# ====== INICIALIZAÇÃO ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)