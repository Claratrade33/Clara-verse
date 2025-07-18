from flask import Flask, render_template, request, jsonify
from binance.client import Client
from binance.enums import *
import openai
import os

# 🔐 Chaves internas blindadas (modo demo com saldo virtual)
openai.api_key = "sk-proj-..."  # (sua chave real vai aqui)
binance_api_key = "8Kr_fake_demo_key_PUBLIC"
binance_secret_key = "Zx12_fake_demo_secret_KEY"

# ⚙️ Ativar modo testnet (Binance Futures demo)
client = Client(binance_api_key, binance_secret_key)
client.API_URL = 'https://testnet.binancefuture.com/fapi'

# ⚙️ Flask app
app = Flask(__name__)

# 🔮 IA Clarinha - Estratégia simples com decisão via GPT
def clarinha_analisa(rsi, preco, tendencia):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é Clarinha, uma IA trader espiritual com alta performance."},
                {"role": "user", "content": f"RSI: {rsi}, Preço: {preco}, Tendência: {tendencia}. O que fazer?"}
            ]
        )
        acao = resposta["choices"][0]["message"]["content"]
        return f"🤖 Clarinha diz: {acao}"
    except Exception as e:
        return f"⚠️ Erro ao consultar Clarinha: {str(e)}"

# 🎯 Executar ordem demo
@app.route("/executar", methods=["POST"])
def executar_ordem():
    try:
        dados = request.json
        par = dados.get("par", "BTCUSDT")
        direcao = dados.get("direcao", "BUY")
        quantidade = float(dados.get("quantidade", 0.001))

        ordem = client.futures_create_order(
            symbol=par,
            side=SIDE_BUY if direcao == "BUY" else SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=quantidade
        )

        return jsonify({
            "status": "sucesso",
            "preco_entrada": ordem["fills"][0]["price"] if "fills" in ordem else "n/a",
            "ordem_id": ordem["orderId"],
            "msg": "Ordem executada com sucesso."
        })
    except Exception as e:
        return jsonify({"status": "erro", "erro": str(e)})

# 📈 Página principal (gráfico, IA e botões)
@app.route("/")
def sala_operacoes():
    return render_template("sala_operacoes.html")

# 🧠 Rota IA Clarinha
@app.route("/consultar-clarinha", methods=["POST"])
def consultar_clarinha():
    dados = request.json
    rsi = dados.get("rsi")
    preco = dados.get("preco")
    tendencia = dados.get("tendencia")
    resposta = clarinha_analisa(rsi, preco, tendencia)
    return jsonify({"resposta": resposta})

# 🌱 Rodando
if __name__ == "__main__":
    app.run(debug=True)

application = app  # render.com