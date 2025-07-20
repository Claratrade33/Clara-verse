from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from binance.client import Client
import os

app = Flask(__name__)
app.secret_key = 'claraverse_super_bunker_key_2025'

# Cliente com API pública da Binance (sem chave)
client = Client()

# Usuário padrão
USUARIO_PADRAO = {
    "username": "admin",
    "password": "claraverse2025"
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    username = request.form['username']
    password = request.form['password']
    if username == USUARIO_PADRAO['username'] and password == USUARIO_PADRAO['password']:
        session['usuario'] = username
        return redirect(url_for('dashboard'))
    return render_template('login.html', erro='Usuário ou senha inválidos')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/dados_binance')
def dados_binance():
    try:
        ticker = client.get_ticker(symbol="BTCUSDT")
        return jsonify(ticker)
    except Exception as e:
        return jsonify({"erro": str(e)})

@app.route('/salvar_chaves', methods=['POST'])
def salvar_chaves():
    dados = request.json
    # Aqui no futuro salvaremos as chaves em local seguro
    return jsonify({"status": "chaves salvas com sucesso (simulado)"})


@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

# ✅ Linha necessária para o Render reconhecer o app Flask
application = app