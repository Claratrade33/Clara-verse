from flask import Flask, render_template_string, request, redirect
import random

app = Flask(__name__)

TOKEN_COMANDANTE = "54E01460FC8BB0AB22FF3DE7"
CADERNO_MISTICO = {
    "Linha 01": "K", "Linha 02": "Y", "Linha 03": "Q", "Linha 04": "L",
    "Linha 05": "R", "Linha 06": "X", "Linha 07": "F", "Linha 08": "E",
    "Linha 09": "M", "Linha 10": "U", "Linha 11": "O", "Linha 12": "G",
    "Linha 13": "Y", "Linha 14": "W", "Linha 15": "5", "Linha 16": "Y"
}
LINHAS_REQUERIDAS = random.sample(list(CADERNO_MISTICO.keys()), 3)

fachada_template = """
<!DOCTYPE html>
<html>
<head>
    <title>ClaraVerse | Entrada</title>
    <style>
        body {
            margin: 0;
            background: #000;
            color: #00ffcc;
            font-family: monospace;
            overflow: hidden;
        }
        iframe {
            position: absolute;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            filter: blur(1px) brightness(0.7);
            pointer-events: none;
            border: none;
        }
        .painel {
            position: absolute;
            top: 15%;
            left: 5%;
            background: rgba(0,0,0,0.5);
            padding: 30px;
            border-radius: 10px;
            border: 1px solid #00ffcc99;
            box-shadow: 0 0 15px #00ffcc88;
            z-index: 10;
        }
        .botao {
            margin-top: 20px;
            background: #00ffcc;
            color: #000;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <iframe src="https://www.tradingview.com/embed-widget/mini-symbol-overview/?symbol=BINANCE:BTCUSDT&locale=br"></iframe>
    <div class="painel">
        <h2>🌌 ClaraVerse</h2>
        <p>Corretora de elite guiada pela IA Clarinha.</p>
        <form method="get" action="/verificar">
            <button class="botao">🔓 Entrar com Token</button>
        </form>
    </div>
</body>
</html>
"""

verificacao_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Verificação</title>
    <style>
        body { background-color: #0e0e0e; color: #fff; font-family: monospace; padding: 40px; }
        input[type=text], input[type=submit] {
            background-color: #111; border: 1px solid #00ffcc; color: #fff;
            padding: 10px; margin: 10px;
        }
        .bloco {
            background: #1a1a1a;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 20px #00ffcc88;
        }
    </style>
</head>
<body>
    <div class="bloco">
        <h2>Entrada Mística</h2>
        <p>Digite as letras do seu Caderno Místico:</p>
        <form method="post">
            {% for linha in linhas %}
                {{ linha }}: <input type="text" name="{{ linha }}" maxlength="1"><br>
            {% endfor %}
            <input type="submit" value="Entrar">
        </form>
        {% if erro %}
            <p style="color:red;">{{ erro }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

sala_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Sala do Comandante</title>
    <style>
        body { background-color: #000; color: #0f0; font-family: monospace; padding: 40px; }
        .painel {
            background: #111;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 12px #00ffcc55;
        }
    </style>
</head>
<body>
    <div class="painel">
        <h1>👨‍🚀 Bem-vindo, Comandante!</h1>
        <p>IA <strong>Clarinha</strong> conectada e aguardando ordens.</p>
        <p>Token verificado. Sistema 100% operacional.</p>
        <p>🔐 Frase-Chave: <em>A Luz que rompe o Véu</em></p>
    </div>
</body>
</html>
"""

@app.route("/")
def fachada():
    return render_template_string(fachada_template)

@app.route("/verificar", methods=["GET", "POST"])
def verificar():
    if request.method == "POST":
        for linha in LINHAS_REQUERIDAS:
            letra = request.form.get(linha, "").upper()
            if letra != CADERNO_MISTICO[linha]:
                return render_template_string(verificacao_template, linhas=LINHAS_REQUERIDAS, erro="Letra incorreta!")
        return redirect("/sala")
    return render_template_string(verificacao_template, linhas=LINHAS_REQUERIDAS, erro=None)

@app.route("/sala")
def sala():
    return render_template_string(sala_template)

# Compatível com gunicorn no Render
application = app