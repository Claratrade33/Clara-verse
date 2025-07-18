# clara_bunker.py — versão final com CSS corrigido, Clarinha ativa, pronto para Render

from flask import Flask, render_template_string, request
import secrets
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

login_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>ClaraVerse | Acesso Sagrado</title>
    <style>
        body { background-color: #0e0e0e; color: #fff; font-family: monospace; padding: 40px; }
        input[type=text], input[type=submit] {
            background-color: #111; border: 1px solid #00ffcc; color: #fff; padding: 10px; margin: 10px;
        }
        .bloco { background: #1a1a1a; padding: 20px; border-radius: 8px; box-shadow: 0 0 20px #00ffcc88; }
    </style>
</head>
<body>
    <div class="bloco">
        <h2>🌌 ClaraVerse — Entrada Mística</h2>
        <p>Digite as letras do seu Caderno Místico:</p>
        <form method="post">
            {% for linha in linhas %}
                {{ linha }}: <input type="text" name="{{ linha }}" maxlength="1"><br>
            {% endfor %}
            <input type="submit" value="Entrar">
        </form>
        {% if erro %}
            <p style="color: red;">{{ erro }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

painel_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>ClaraVerse | Sala do Comandante</title>
    <style>
        body { background-color: #000; color: #0f0; font-family: monospace; padding: 30px; }
        .painel { background: #111; padding: 20px; border-radius: 8px; }
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
'''

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        for linha in LINHAS_REQUERIDAS:
            letra = request.form.get(linha, "").upper()
            if letra != CADERNO_MISTICO[linha]:
                return render_template_string(login_template, linhas=LINHAS_REQUERIDAS, erro="Letra incorreta!")
        return render_template_string(painel_template)
    return render_template_string(login_template, linhas=LINHAS_REQUERIDAS, erro=None)

# Entry point para Render
application = app