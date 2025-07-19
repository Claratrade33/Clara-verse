from flask import Flask, request, render_template_string
from binance.client import Client
import os

app = Flask(__name__)

# Chaves fixas (já criptografadas ou testnet por padrão)
API_KEY = os.getenv("Bia", "sua_api_demo_aqui")
API_SECRET = os.getenv("Bia1", "sua_secret_demo_aqui")
client = Client(API_KEY, API_SECRET, testnet=True)

# Template HTML com painel completo
template_html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ClaraVerse | Sala de Operações</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #0d0d0d; color: #eee; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; }
        .painel { padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .botao { margin: 10px; padding: 15px 30px; border: none; font-size: 16px; border-radius: 5px; cursor: pointer; background: #00ffcc; color: #000; }
        .botao:hover { background: #00bfa6; }
        .input-meta { padding: 10px; font-size: 16px; margin-bottom: 15px; width: 200px; }
        .resultado, .historico { margin-top: 20px; padding: 15px; background: #111; border-radius: 10px; max-width: 500px; width: 90%; }
        .ordem { margin-top: 10px; border-left: 4px solid #00ffcc; padding-left: 10px; }
    </style>
</head>
<body>
    <div class="painel">
        <h1>🧠 ClarinhaBubi em Ação</h1>
        <form method="POST" action="/configurar">
            <input class="input-meta" type="text" name="meta" placeholder="Meta diária em USDT" required>
            <button class="botao" type="submit">Salvar Meta</button>
        </form>

        <form method="POST" action="/executar">
            <button class="botao" type="submit">🚀 Executar Ordem</button>
        </form>

        <form method="POST" action="/stop">
            <button class="botao" type="submit" style="background:red;color:white">🛑 STOP</button>
        </form>

        {% if resultado %}
        <div class="resultado">
            <h3>Resultado da Última Ordem</h3>
            <p><strong>Preço de Entrada:</strong> {{ resultado.preco }}</p>
            <p><strong>Lucro:</strong> {{ resultado.lucro }}</p>
            <p><strong>ROI:</strong> {{ resultado.roi }}%</p>
        </div>
        {% endif %}

        {% if historico %}
        <div class="historico">
            <h3>Histórico de Ordens</h3>
            {% for ordem in historico %}
            <div class="ordem">
                <p>Moeda: {{ ordem.moeda }}</p>
                <p>Lucro: {{ ordem.lucro }}</p>
                <p>ROI: {{ ordem.roi }}%</p>
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# Variáveis simuladas (em memória)
meta_lucro = 0
historico_ordens = []

@app.route("/")
def index():
    return render_template_string(template_html, resultado=None, historico=historico_ordens)

@app.route("/configurar", methods=["POST"])
def configurar():
    global meta_lucro
    meta_lucro = float(request.form.get("meta", 0))
    return render_template_string(template_html, resultado=None, historico=historico_ordens)

@app.route("/executar", methods=["POST"])
def executar_ordem():
    # Simulação de execução com resultado fixo
    preco = 1000
    lucro = 43.55
    roi = 4.35
    resultado = {"preco": preco, "lucro": f"{lucro:.2f}", "roi": f"{roi:.2f}"}
    historico_ordens.append({"moeda": "BTCUSDT", "lucro": lucro, "roi": roi})
    return render_template_string(template_html, resultado=resultado, historico=historico_ordens)

@app.route("/stop", methods=["POST"])
def parar_ordem():
    resultado = {"preco": 1010, "lucro": -20.00, "roi": -1.8}
    historico_ordens.append({"moeda": "BTCUSDT", "lucro": -20.00, "roi": -1.8})
    return render_template_string(template_html, resultado=resultado, historico=historico_ordens)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)