import os
from flask import Flask, render_template_string, request, jsonify
from cryptography.fernet import Fernet
from binance.client import Client
from openai import OpenAI

# CHAVE FERNET USADA PARA DESCRIPTOGRAFAR
FERNET_KEY = "0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="
fernet = Fernet(FERNET_KEY.encode())

try:
    API_KEY = fernet.decrypt(os.getenv("Bia").encode()).decode()
    API_SECRET = fernet.decrypt(os.getenv("Bia1").encode()).decode()
    OPENAI_KEY = fernet.decrypt(os.getenv("OPEN").encode()).decode()
except Exception as e:
    raise Exception(f"Erro ao descriptografar as chaves: {str(e)}")

# INICIALIZAÇÃO
app = Flask(__name__)
binance = Client(API_KEY, API_SECRET)
client_openai = OpenAI(api_key=OPENAI_KEY)

# INTERFACE HTML EMBUTIDA
html = '''
<!DOCTYPE html>
<html>
<head>
    <title>ClaraVerse - Sala de Operações</title>
    <style>
        body { background-color: #000; color: #0f0; font-family: monospace; text-align: center; }
        button { margin: 10px; padding: 20px; font-size: 18px; background: #111; color: #0f0; border: 1px solid #0f0; }
    </style>
</head>
<body>
    <h1>💹 ClaraVerse - Sala de Operações 💻</h1>
    <button onclick="acionar('entrada')">ENTRADA</button>
    <button onclick="acionar('stop')">STOP</button>
    <button onclick="acionar('alvo')">ALVO</button>
    <button onclick="acionar('configurar')">CONFIGURAR</button>
    <button onclick="acionar('automatico')">AUTOMÁTICO</button>
    <pre id="resposta"></pre>
    <script>
        async function acionar(botao) {
            const res = await fetch('/botao', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ acao: botao })
            });
            const data = await res.json();
            document.getElementById('resposta').innerText = JSON.stringify(data, null, 2);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html)

@app.route('/botao', methods=['POST'])
def botao():
    acao = request.json.get('acao')
    if acao == "entrada":
        return jsonify({"status": "executando ENTRADA", "acao": acao})
    elif acao == "stop":
        return jsonify({"status": "executando STOP", "acao": acao})
    elif acao == "alvo":
        return jsonify({"status": "executando ALVO", "acao": acao})
    elif acao == "configurar":
        return jsonify({"config": {
            "par": "BTC/USDT",
            "modelo": "GPT-4o",
            "modo": "manual"
        }})
    elif acao == "automatico":
        return jsonify({"status": "modo AUTOMÁTICO ativado"})
    else:
        return jsonify({"erro": "ação inválida"})

# FLASK COMPATÍVEL COM GUNICORN
application = app
