import os
from flask import Flask, render_template_string, request, redirect
from binance.client import Client
import datetime
import random

# ==========================
# 🔐 Chaves da Binance (reais, protegidas)
# ==========================
API_KEY = "j4nBvFRELeSFDDpgMIz35yTW5JZyNIVIRDPc8Nrt2jmZHWdZRpgGHGxnIzIJeMnK"
API_SECRET = "jkTxQjEtD0mgWxFeM2I2pxXsZimhnGEeWEN2MTz8Y5w7Y00gCVmjLrV3vFo8REKy"

# ==========================
# 🤖 IA ClarinhaBubi Ativa
# ==========================
modo_automatico = False
meta_lucro = 50.0
historico_operacoes = []
saldo_inicial_demo = 10000.0
saldo_atual_demo = saldo_inicial_demo

# ==========================
# 🚀 Inicialização do app Flask
# ==========================
app = Flask(__name__)

client = Client(API_KEY, API_SECRET, testnet=False)

# ==========================
# 🎯 Rota Principal
# ==========================
@app.route("/", methods=["GET", "POST"])
def index():
    global modo_automatico, meta_lucro, historico_operacoes, saldo_atual_demo

    if request.method == "POST":
        if "configurar" in request.form:
            meta_lucro = float(request.form.get("meta", 50))
        elif "executar" in request.form:
            resultado = executar_ordem()
            historico_operacoes.insert(0, resultado)
        elif "automatico" in request.form:
            modo_automatico = not modo_automatico
        elif "stop" in request.form:
            modo_automatico = False

    roi = calcular_roi()
    return render_template_string(template_html,
        modo=modo_automatico,
        meta=meta_lucro,
        roi=roi,
        historico=historico_operacoes[:5]
    )

# ==========================
# 📉 Execução de Ordem Simples
# ==========================
def executar_ordem():
    global saldo_atual_demo

    par = "BTCUSDT"
    ticker = client.get_symbol_ticker(symbol=par)
    preco = float(ticker['price'])

    direcao = random.choice(["COMPRA", "VENDA"])
    resultado = random.uniform(-15, 25)
    saldo_atual_demo += resultado

    return {
        "data": datetime.datetime.now().strftime("%d/%m %H:%M"),
        "preco": round(preco, 2),
        "direcao": direcao,
        "resultado": round(resultado, 2),
        "novo_saldo": round(saldo_atual_demo, 2)
    }

# ==========================
# 📊 Cálculo de ROI
# ==========================
def calcular_roi():
    ganho = saldo_atual_demo - saldo_inicial_demo
    return round((ganho / saldo_inicial_demo) * 100, 2)

# ==========================
# 🌐 Executar no Render
# ==========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

# ==========================
# 🎨 Template HTML
# ==========================
template_html = """
<!DOCTYPE html>
<html>
<head>
    <title>ClaraVerse | Sala de Operações</title>
    <meta charset="UTF-8">
    <style>
        body {
            background-color: #000;
            color: #0ff;
            font-family: 'Courier New', monospace;
            padding: 30px;
        }
        h1 { color: #fff; }
        .painel { border: 1px solid #0ff; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .botao { padding: 10px 20px; margin: 10px; background: #0ff; color: #000; border: none; border-radius: 5px; cursor: pointer; }
        .botao:hover { background: #fff; }
        .postit {
            background: #111;
            border-left: 6px solid #0ff;
            padding: 10px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <h1>🚀 ClaraVerse - IA ClarinhaBubi</h1>
    <div class="painel">
        <form method="POST">
            <label>Meta de Lucro por Sessão (USDT):</label>
            <input type="number" name="meta" value="{{ meta }}">
            <button class="botao" name="configurar">Salvar Meta</button>
        </form>
        <p><strong>Modo:</strong> {{ 'Automático' if modo else 'Manual' }}</p>
        <form method="POST">
            <button class="botao" name="executar">Executar Ordem</button>
            <button class="botao" name="automatico">{{ 'Parar Automático' if modo else 'Ativar Automático' }}</button>
            <button class="botao" name="stop">🛑 STOP</button>
        </form>
    </div>

    <div class="painel">
        <h3>📈 ROI Atual: {{ roi }}%</h3>
        <h3>📜 Últimas Operações:</h3>
        {% for ordem in historico %}
            <div class="postit">
                📅 {{ ordem.data }} | {{ ordem.direcao }} @ {{ ordem.preco }}  
                → Resultado: <strong>{{ ordem.resultado }} USDT</strong><br>
                Saldo Atual: {{ ordem.novo_saldo }} USDT
            </div>
        {% endfor %}
    </div>
</body>
</html>
"""