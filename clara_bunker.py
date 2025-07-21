import os
from flask import Flask, request, jsonify, render_template
from binance.client import Client
import openai
from cryptography.fernet import Fernet

# CHAVE FERNET
FERNET_KEY = "ylh-urjGFbF60dGJcGjEWY5SKGbhui-8SUItRz7YMZk="
fernet = Fernet(FERNET_KEY.encode())

# CHAVES CRIPTOGRAFADAS
API_KEY = fernet.decrypt(b"gAAAAABoe_tmC3u_LkLDxTnp5p-7wgMiHVcKvJIOgEQFfBTWjRx5CC2Ts3Z1PPx-vEA1ChEFZMxi1THdulmp8WK8wCJzBmS8vHAWEU4pooCBt8tVrlf0NkfOur-pEtjpjZt6NSpPUbhFvIqjtwNDnQAtMQL_mPfM8Dype0oShNoTkcMnECOsmF0=").decode()
API_SECRET = fernet.decrypt(b"gAAAAABoe_tmrN2tKPQsPVYlnxp-wKItqZNirJXN_9eKHhle-_z_eud6i1pGpdG-ZRsDf_g26q2jlRixSXv8h_ZwOv5p4lu3AshCRbHXRpPvcHJ8LaoqGOP2ZQNH4h-8WUdPOSlEXYz2NXJHOlYMigWiyZO8d2w0NYlQa0N2Vv-CpDMOXuIXcN8=").decode()
OPENAI_KEY = fernet.decrypt(b"gAAAAABoe_xqx7jAACfbXHrmoFSrEU_x2uJbVsrYNvjpn-IWOD02jHr6pAtSznZZkFd0cE50OcdsFukYMR441vQgThN8UaoeQXvbD76jS3wJkvlcGJcwfbwWOi2dEd9MgZuEULE92B9UYLFVzgKzP3ZJ-IRmsF_ppg==").decode()

# CLIENTES
binance = Client(API_KEY, API_SECRET)
openai.api_key = OPENAI_KEY

# Instância da aplicação Flask
application = Flask(__name__)

# Rotas para as páginas HTML
@application.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@application.route("/configurar", methods=["GET"])
def configurar():
    return render_template("configurar.html")

@application.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@application.route("/painel", methods=["GET"])
def painel():
    return render_template("painel.html")

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