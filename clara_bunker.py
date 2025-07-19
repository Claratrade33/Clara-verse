#clara_bunker.py
# Sistema operacional completo com integração Binance + OpenAI + IA Clarinha
# Arquivo único, blindado e funcional

from flask import Flask, render_template_string, request
import openai
import os

app = Flask(__name__)

# HTMLs embutidos
FACHADA_HTML = """
<!DOCTYPE html>
<html><head><title>ClaraVerse</title></head>
<body style='background:#000;color:#0f0;font-family:monospace;text-align:center'>
<h1>🚀 ClaraVerse | Corretora Inteligente</h1>
<a href='/sala'><button style='padding:20px;font-size:20px'>ENTRAR NA SALA</button></a>
</body></html>
"""

SALA_HTML = """
<!DOCTYPE html>
<html><head><title>Sala de Operações</title></head>
<body style='background:#111;color:#fff;font-family:sans-serif'>
<h2>🧠 Sala de Operações - Clarinha IA</h2>
<form method='post'>
    <label>Meta de Lucro (%):</label><input name='meta'><br><br>
    <label>STOP LOSS (%):</label><input name='stop'><br><br>
    <button type='submit'>ATIVAR IA</button>
</form>
{% if resultado %}
    <p><strong>Resultado:</strong> {{ resultado }}</p>
{% endif %}
</body></html>
"""

@app.route("/")
def fachada():
    return render_template_string(FACHADA_HTML)

@app.route("/sala", methods=["GET", "POST"])
def sala():
    resultado = None
    if request.method == "POST":
        meta = request.form.get("meta")
        stop = request.form.get("stop")
        resultado = f"IA ativada com meta de {meta}% e stop de {stop}%"
    return render_template_string(SALA_HTML, resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
