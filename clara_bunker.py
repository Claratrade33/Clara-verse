import os
from flask import Flask, render_template_string, request
from binance.client import Client
from cryptography.fernet import Fernet
import openai

# 🔐 Chave Fernet e credenciais criptografadas
FERNET_KEY = b'0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA='
api_key_criptografada = b'gAAAAABm...'
api_secret_criptografada = b'gAAAAABm...'
openai_key = 'sk-...'

# 🔓 Descriptografando as chaves
chave_fernet = Fernet(FERNET_KEY)
api_key = chave_fernet.decrypt(api_key_criptografada).decode()
api_secret = chave_fernet.decrypt(api_secret_criptografada).decode()

# 🤖 Configurações
modo_demo = True
saldo_demo = 10000
par_moeda = "BTCUSDT"
meta_lucro = 15

# 🤝 Conectar à Binance Testnet
if modo_demo:
    client = Client(api_key, api_secret, testnet=True)
    client.API_URL = 'https://testnet.binancefuture.com'
else:
    client = Client(api_key, api_secret)

# 🔮 ClarinhaBubi — IA de Operações
openai.api_key = openai_key
def clarinha_responde(pergunta):
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é uma trader especialista chamada ClarinhaBubi, direta e intuitiva."},
            {"role": "user", "content": pergunta}
        ]
    )
    return resposta.choices[0].message["content"]

# 🚀 Iniciar app Flask
app = Flask(__name__)

# 🎯 Página principal
@app.route("/", methods=["GET", "POST"])
def painel():
    resultado_ordem = ""
    if request.method == "POST":
        acao = request.form.get("acao")
        if acao == "executar":
            resultado_ordem = executar_ordem()
        elif acao == "automatico":
            resultado_ordem = modo_automatico()
    return render_template_string(html, resultado=resultado_ordem)

# 📈 Estratégia Manual
def executar_ordem():
    try:
        preco = float(client.futures_mark_price(symbol=par_moeda)['markPrice'])
        quantidade = round(10 / preco, 3)
        ordem_compra = client.futures_create_order(
            symbol=par_moeda,
            side='BUY',
            type='MARKET',
            quantity=quantidade
        )
        return f"Ordem executada: COMPRA {quantidade} {par_moeda} a {preco:.2f} USDT"
    except Exception as e:
        return f"Erro ao executar ordem: {str(e)}"

# 🤖 Estratégia Automática com Clarinha
def modo_automatico():
    analise = clarinha_responde(f"Qual direção devo operar {par_moeda} agora?")
    if "compr" in analise.lower():
        return executar_ordem()
    elif "vend" in analise.lower():
        return vender_ordem()
    else:
        return "ClarinhaBubi sugeriu aguardar. ✋"

def vender_ordem():
    try:
        preco = float(client.futures_mark_price(symbol=par_moeda)['markPrice'])
        quantidade = round(10 / preco, 3)
        ordem_venda = client.futures_create_order(
            symbol=par_moeda,
            side='SELL',
            type='MARKET',
            quantity=quantidade
        )
        return f"Ordem executada: VENDA {quantidade} {par_moeda} a {preco:.2f} USDT"
    except Exception as e:
        return f"Erro ao vender: {str(e)}"

# 🧬 HTML com gráfico e botões
html = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ClaraVerse - Sala de Operações Elite com ClarinhaBubi 🚀</title>
    <style>
        body {
            background: linear-gradient(145deg, #0f2027, #203a43, #2c5364);
            color: #ffffff;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
        }
        .painel {
            margin-top: 40px;
        }
        iframe {
            width: 90%;
            height: 480px;
            border: none;
            border-radius: 10px;
        }
        button {
            background: #00ffc8;
            border: none;
            color: #000;
            font-size: 18px;
            padding: 14px 28px;
            margin: 20px 10px;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 0 20px #00ffc855;
        }
        .resultado {
            margin-top: 20px;
            font-size: 18px;
            color: #00ffcc;
        }
    </style>
</head>
<body>
    <h1>🚀 ClaraVerse - Sala de Operações Elite com ClarinhaBubi 🚀</h1>
    <div class="painel">
        <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview&symbol=BINANCE:BTCUSDT&interval=1&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=rgba(0,0,0,1)&studies=[]&theme=dark&style=1&timezone=Etc/UTC&studies_overrides={}" allowfullscreen></iframe>
    </div>
    <form method="post">
        <button name="acao" value="executar">Executar Ordem</button>
        <button name="acao" value="automatico">Modo Automático</button>
    </form>
    {% if resultado %}
        <div class="resultado">📊 {{ resultado }}</div>
    {% endif %}
</body>
</html>
'''

# Render exige essa linha:
application = app