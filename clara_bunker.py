import os
from flask import Flask, request, jsonify, render_template_string
from binance.client import Client
from openai import OpenAI
from cryptography.fernet import Fernet

# ======= FERNET KEY =======
FERNET_KEY = "0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="
fernet = Fernet(FERNET_KEY.encode())

# ======= CHAVES CRIPTOGRAFADAS =======
API_KEY = fernet.decrypt(b"gAAAAABofAOtwLRJJhSH1aUN9ywCdygAroOP5dcNt4KeGFwI0WTS_oJyqng2VIXEQimQN7SIf1lyfTmzW699MRPcyAZrnODRr-wCD2g7Opgo2zOHxPr1FN4HHhUI_o2il7jwfp4djNGfrvxMlHRky7dR9iZdXwsiaU2mz8eAr6RCvaxHfj34-Xo=").decode()
API_SECRET = fernet.decrypt(b"gAAAAABofAOt-LdSyc_aH5i0KhlpPxGYI-eJfPz4grMf57YOPyu0ux9Eza9OBy_ZfKaIU6bVMFIzc6MIwRPuiwA3JwSBcWyOIOp2_aq4mNOSS4atSzUsMibliAtyoTeswzg1Q2CaW8uq5YpY_vFtk219dHGz1hJYt9AE_5M_pigUTiKD6YAfvR8=").decode()
OPENAI_KEY = fernet.decrypt(b"gAAAAABofAOt2kA847ZWvf52ZnqnwmvZ8CUyf8x8THt5mZ_xddw5fipKV0MGmFzOo2NSHgggxin_t2MUm3kUozs13lfvvZKQzA==").decode()

# ======= CLIENTES =======
app = Flask(__name__)
binance = Client(API_KEY, API_SECRET)
client_openai = OpenAI(api_key=OPENAI_KEY)

# ======= HTML UI =======
html = """
<!doctype html>
<html>
<head><title>ClaraVerse Bunker</title></head>
<body style="background-color:#0d1117; color:white; font-family:sans-serif; text-align:center; padding:30px;">
    <h1>👁️ ClaraVerse</h1>
    <h3>Sala de operações</h3>
    <button onclick="enviarAcao('entrada')">ENTRADA</button>
    <button onclick="enviarAcao('alvo')">ALVO</button>
    <button onclick="enviarAcao('stop')">STOP</button>
    <button onclick="enviarAcao('auto')">AUTOMÁTICO</button>
    <div id="resposta" style="margin-top:20px;"></div>

    <script>
    function enviarAcao(acao) {
        fetch('/acao', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ acao: acao })
        })
        .then(r => r.json())
        .then(d => {
            document.getElementById('resposta').innerText = JSON.stringify(d, null, 2);
        });
    }
    </script>
</body>
</html>
"""

# ======= ROTA PRINCIPAL =======
@app.route("/")
def index():
    return render_template_string(html)

@app.route("/acao", methods=["POST"])
def acao():
    dados = request.get_json()
    acao = dados.get("acao")

    if acao == "auto":
        resultado = gerar_ordem()
    else:
        resultado = {"mensagem": f"Ação manual: {acao}"}

    return jsonify(resultado)

# ======= LÓGICA DE ORDEM (AUTO) =======
def gerar_ordem():
    prompt = (
        "Você é um analista de operações. Gere uma análise JSON para os pares BTC/USDT, PEPE/USDT e SUI/USDT. "
        "Formato:\n"
        "{\n"
        "  \"par\": \"BTC/USDT\",\n"
        "  \"entrada\": valor,\n"
        "  \"alvo\": valor,\n"
        "  \"stop\": valor,\n"
        "  \"confianca\": \"alta|media|baixa\"\n"
        "}"
    )
    resposta = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"auto": resposta.choices[0].message.content}

# ======= APP =======
app = app
