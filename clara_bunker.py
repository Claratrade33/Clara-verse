from flask import Flask, render_template, request, redirect, session, jsonify
from cryptography.fernet import Fernet
from datetime import timedelta
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(hours=6)

CHAVE_CRIPTO_FIXA = b'xApbCQFxxa3Yy3YKkzP9JkkfE4WaXxN8eSpK7uBRuGA='
fernet = Fernet(CHAVE_CRIPTO_FIXA)

usuarios = {'admin': 'claraverse2025'}
chaves_armazenadas = {}
chave_arquivo = 'chaves.dat'
saldo_simulado = 10000.00
modo_auto_ativo = False

def carregar_chaves():
    global chaves_armazenadas
    if os.path.exists(chave_arquivo):
        with open(chave_arquivo, 'rb') as f:
            dados = f.read()
            descriptografado = fernet.decrypt(dados).decode()
            chaves_armazenadas = json.loads(descriptografado)

def salvar_chaves_em_arquivo():
    dados = json.dumps(chaves_armazenadas).encode()
    criptografado = fernet.encrypt(dados)
    with open(chave_arquivo, 'wb') as f:
        f.write(criptografado)

@app.route('/salvar_chaves', methods=['POST'])
def salvar_chaves():
    dados = request.json
    try:
        if not dados.get('openaiKey') or not dados.get('binanceKey') or not dados.get('binanceSecret'):
            return jsonify({'status': 'erro', 'mensagem': 'Todos os campos devem ser preenchidos.'}), 400

        chaves_armazenadas['openai'] = fernet.encrypt(dados['openaiKey'].encode()).decode()
        chaves_armazenadas['binance'] = fernet.encrypt(dados['binanceKey'].encode()).decode()
        chaves_armazenadas['binance_secret'] = fernet.encrypt(dados['binanceSecret'].encode()).decode()
        salvar_chaves_em_arquivo()
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

# Carrega as chaves da memória criptografada
carregar_chaves()

if __name__ == '__main__':
    app.run(debug=True)