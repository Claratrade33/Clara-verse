import os
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for
from binance.client import Client
import openai
from cryptography.fernet import Fernet

# CHAVE FERNET
FERNET_KEY = "ylh-urjGFbF60dGJcGjEWY5SKGbhui-8SUItRz7YMZk="
fernet = Fernet(FERNET_KEY.encode())

# CLIENTES
application = Flask(__name__)

# Variáveis globais para chaves API
API_KEY = None
API_SECRET = None
OPENAI_KEY = None
binance = None

# Rotas para as páginas HTML
@application.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for('painel'))
    return render_template("login.html")

@application.route("/painel", methods=["GET"])
def painel():
    global binance, openai
    if not API_KEY or not API_SECRET or not OPENAI_KEY:
        return redirect(url_for('configurar'))
    
    binance = Client(API_KEY, API_SECRET)
    openai.api_key = OPENAI_KEY
    
    return render_template("painel.html")

@application.route("/configurar", methods=["GET", "POST"])
def configurar():
    if request.method == "POST":
        global API_KEY, API_SECRET, OPENAI_KEY
        data = request.form
        API_KEY = data['binanceApiKey']
        API_SECRET = data['binanceSecretKey']
        OPENAI_KEY = data['openaiKey']
        
        # Salvar as chaves em um arquivo
        with open('config.json', 'w') as config_file:
            json.dump({
                'openai_key': OPENAI_KEY,
                'binance_api_key': API_KEY,
                'binance_secret_key': API_SECRET
            }, config_file)

        return redirect(url_for('painel'))
    
    return render_template("configurar.html")

# Endpoints da API
@application.route('/obter_preco', methods=['GET'])
def obter_preco():
    try:
        ticker = binance.get_symbol_ticker(symbol="BTCUSDT")
        return jsonify({'preco': ticker['price']})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@application.route('/obter_saldo', methods=['GET'])
def obter_saldo():
    try:
        account_info = binance.get_account()
        usdt_balance = next((item for item in account_info['balances'] if item['asset'] == 'USDT'), None)
        return jsonify({'saldo': usdt_balance['free'] if usdt_balance else 0})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@application.route('/executar_acao', methods=['POST'])
def executar_acao():
    data = request.json
    acao = data.get('acao')
    
    try:
        if acao == 'comprar':
            order = binance.order_market_buy(symbol='BTCUSDT', quantity=0.001)
            return jsonify({'mensagem': 'Compra realizada com sucesso!', 'detalhes': order})
        elif acao == 'vender':
            order = binance.order_market_sell(symbol='BTCUSDT', quantity=0.001)
            return jsonify({'mensagem': 'Venda realizada com sucesso!', 'detalhes': order})
        else:
            return jsonify({'mensagem': 'Ação inválida'}), 400
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@application.route('/obter_sugestao_ia', methods=['GET'])
def obter_sugestao_ia():
    try:
        prompt = "Sugira uma ação de trading para o par BTC/USDT."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({'resposta': response.choices[0].message.content})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=7860)