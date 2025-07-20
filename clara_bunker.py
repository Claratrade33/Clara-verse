from flask import Flask, render_template, request, redirect, session
import os, json

app = Flask(__name__)
app.secret_key = 'claraverse-secure-key'

CHAVE_PATH = 'modelos/chaves.json'

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['usuario'] == 'admin' and request.form['senha'] == 'claraverse2025':
            session['logado'] = True
            return redirect('/painel')
        else:
            return render_template('login.html', erro='Credenciais inválidas.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if not session.get('logado'):
        return redirect('/login')
    return render_template('dashboard.html')

@app.route('/painel')
def painel():
    if not session.get('logado'):
        return redirect('/login')
    return render_template('painel.html')

@app.route('/configurar', methods=['GET'])
def configurar():
    if not session.get('logado'):
        return redirect('/login')
    return render_template('configurar.html')

@app.route('/salvar_chaves', methods=['POST'])
def salvar_chaves():
    if not session.get('logado'):
        return redirect('/login')
    chaves = {
        "binance_api_key": request.form.get("binance_api_key"),
        "binance_api_secret": request.form.get("binance_api_secret"),
        "openai_api_key": request.form.get("openai_api_key")
    }
    with open(CHAVE_PATH, "w") as f:
        json.dump(chaves, f)
    return redirect('/painel')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)