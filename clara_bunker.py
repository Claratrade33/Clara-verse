import os
from flask import Flask, request, jsonify, render_template_string
from cryptography.fernet import Fernet
from binance.client import Client
from openai import OpenAI

# 🔐 FERNET DECRIPTAÇÃO
FERNET_KEY = "INSIRA_SUA_CHAVE_FERNET_BASE64_AQUI"  # Substitua por sua chave de 32 bytes em Base64
fernet = Fernet(FERNET_KEY.encode())

try:
    API_KEY = fernet.decrypt(os.getenv("Bia").encode()).decode()
    API_SECRET = fernet.decrypt(os.getenv("Bia1").encode()).decode()
    OPENAI_KEY = fernet.decrypt(os.getenv("OPEN").encode()).decode()
except Exception as e:
    raise Exception(f"Erro ao descriptografar as chaves: {str(e)}")

# 🔧 INICIALIZAÇÕES
app = Flask(__name__)
binance = Client(API_KEY, API_SECRET)
client_openai = OpenAI(api_key=OPENAI_KEY)

# 📊 INTERFACE HTML EMBUTIDA
html = """
<!DOCTYPE html>
<html>
<head>
    <title>ClaraVerse - Bunker de Operações</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #111; color: #eee; text-align: center; }
        .botao { padding: 12px 24px; margin: 10px; font-size: 18px; background-color: #222; color: #00ffcc; border: 2px solid #00ffcc; border-radius: 5px; cursor: pointer; }
        .botao:hover { background-color: #00ffcc; color: #111; }
        #resposta { margin-top: 20px; font-size: 18px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>🛡️ ClaraVerse - Sala de Operações 🧠</h1>
    <p>Escolha uma ação:</p>
    <button class="botao" onclick="enviarComando('ENTRADA')">📈 ENTRADA</button>
    <button class="botao" onclick="enviarComando('STOP')">⛔ STOP</button>
    <button class="botao" onclick="enviarComando('ALVO')">🎯 ALVO</button>
    <button class="botao" onclick="enviarComando('AUTOMÁTICO')">🤖 AUTOMÁTICO</button>
    <div id="resposta"></div>

    <script>
        async function enviarComando(acao) {
            const respostaDiv = document.getElementById('resposta');
            respostaDiv.innerHTML = '⏳ Processando...';
            const res = await fetch('/comando', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ acao })
            });
            const data = await res.json();
            respostaDiv.innerHTML = '<strong>🔍 Resultado:</strong><br>' + JSON.stringify(data, null, 2);
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html)

@app.route("/comando", methods=["POST"])
def comando():
    acao = request.json.get("acao", "").upper()

    if acao == "ENTRADA":
        return jsonify(entrada())

    elif acao == "STOP":
        return jsonify({"stop": "Em desenvolvimento, Clarinha avisa 😇"})

    elif acao == "ALVO":
        return jsonify({"alvo": "Logo ali na lua 🌕"})

    elif acao == "AUTOMÁTICO":
        return jsonify(automacao())

    else:
        return jsonify({"erro": "Ação desconhecida"})

def entrada():
    try:
        candles = binance.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, limit=5)
        preco_atual = float(candles[-1][4])

        prompt = f"""
        Com base no preço atual do BTC/USDT ({preco_atual}), retorne em JSON a estratégia:
        {{
            "entrada": <preço ideal>,
            "alvo": <preço para lucro>,
            "stop": <preço para stop loss>,
            "confianca": <nível de confiança de 0 a 100>
        }}
        """

        resposta = client_openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é uma IA especialista em trading de criptomoedas."},
                {"role": "user", "content": prompt}
            ]
        )

        conteudo = resposta.choices[0].message.content.strip()
        return eval(conteudo)  # Pode substituir por json.loads se retornar JSON válido

    except Exception as e:
        return {"erro": str(e)}

def automacao():
    return {"status": "🔄 Modo automático ativado! (Em testes ainda...)"}

# ✅ Corrige o erro de importação com Gunicorn
if __name__ == "__main__":
    app.run(debug=True)

application = app  # ← ESSENCIAL para Render + Gunicorn funcionar!
