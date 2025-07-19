# clara_bunker.py

from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# HTML embutido (versão resumida para demonstração)
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>ClaraVerse | Sala de Operações</title>
    <style>
        body { background-color: #0f0f0f; color: #fff; font-family: Arial; text-align: center; }
        .painel { margin-top: 50px; }
        button { margin: 10px; padding: 20px; font-size: 18px; background: #00ffcc; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="painel">
        <h1>ClaraVerse - IA ClarinhaBubi Operando</h1>
        <button onclick="fetch('/executar').then(r => r.json()).then(d => alert(d.status))">ENTRADA</button>
        <button onclick="fetch('/stop').then(r => r.json()).then(d => alert(d.status))">STOP</button>
        <button onclick="fetch('/alvo').then(r => r.json()).then(d => alert(d.status))">ALVO</button>
        <button onclick="fetch('/configurar').then(r => r.json()).then(d => alert(d.status))">CONFIGURAR</button>
        <button onclick="fetch('/automatico').then(r => r.json()).then(d => alert(d.status))">AUTOMÁTICO</button>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/executar')
def executar():
    # Simulação da lógica de entrada
    return jsonify({"status": "Ordem de ENTRADA executada com sucesso!"})

@app.route('/stop')
def stop():
    # Simulação de STOP
    return jsonify({"status": "STOP acionado com sucesso!"})

@app.route('/alvo')
def alvo():
    # Simulação de alvo
    return jsonify({"status": "Alvo de lucro definido!"})

@app.route('/configurar')
def configurar():
    # Simulação de configuração
    return jsonify({"status": "Painel de configuração aberto!"})

@app.route('/automatico')
def automatico():
    # Simulação de modo automático
    return jsonify({"status": "Modo automático ativado com ClarinhaBubi!"})

# Executar no Render com Gunicorn
application = app

if __name__ == '__main__':
    app.run(debug=True)