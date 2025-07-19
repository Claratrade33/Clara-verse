import os
from flask import Flask, render_template_string, request, jsonify
from cryptography.fernet import Fernet
from binance.client import Client
from openai import OpenAI

# ======================= CHAVE DE CRIPTOGRAFIA ===========================
FERNET_KEY = "0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="
fernet = Fernet(FERNET_KEY.encode())

# =================== FUNÇÃO DE MODO LOCAL: GERAR .env ====================
def gerar_variaveis_criptografadas():
    print("\n🔐 Modo de criptografia interativa ativado.\n")
    openai_key = input("Digite sua chave OPENAI: ")
    binance_key = input("Digite sua API KEY Binance: ")
    binance_secret = input("Digite sua SECRET Binance: ")

    encrypted_openai = fernet.encrypt(openai_key.encode()).decode()
    encrypted_binance_key = fernet.encrypt(binance_key.encode()).decode()
    encrypted_binance_secret = fernet.encrypt(binance_secret.encode()).decode()

    print("\n📋 Cole essas variáveis no Render (.env):\n")
    print(f"OPEN={encrypted_openai}")
    print(f"Bia={encrypted_binance_key}")
    print(f"Bia1={encrypted_binance_secret}")
    exit()

# =========== DETECTA SE ESTÁ LOCAL (SEM VARIÁVEIS SETADAS) ==============
if not os.getenv("Bia") or not os.getenv("Bia1") or not os.getenv("OPEN"):
    gerar_variaveis_criptografadas()

# ======================== DESCRIPTOGRAFIA DAS CHAVES =====================
try:
    API_KEY = fernet.decrypt(os.getenv("Bia").encode()).decode()
    API_SECRET = fernet.decrypt(os.getenv("Bia1").encode()).decode()
    OPENAI_KEY = fernet.decrypt(os.getenv("OPEN").encode()).decode()
except Exception as e:
    raise Exception(f"❌ Erro ao descriptografar as chaves: {str(e)}")

# =========================== INICIALIZAÇÕES ==============================
app = Flask(__name__)
binance = Client(API_KEY, API_SECRET)
client_openai = OpenAI(api_key=OPENAI_KEY)

# ============================= INTERFACE =================================
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

# ============================ ROTAS FLASK ================================
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

# ========================= PARA GUNICORN NO RENDER =======================
application = app
