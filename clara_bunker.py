from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'clarinha-super-bunker'

# Usuário padrão
USUARIO_PADRAO = {'username': 'admin', 'password': 'claraverse2025'}

# Rota inicial redireciona para login
@app.route('/')
def home():
    return redirect(url_for('login'))

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USUARIO_PADRAO['username'] and password == USUARIO_PADRAO['password']:
            session['usuario'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', erro='Credenciais inválidas')
    return render_template('login.html')

# Painel protegido (dashboard)
@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return render_template('dashboard.html', usuario=session['usuario'])
    return redirect(url_for('login'))

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

# Rota para salvar chaves (exemplo)
@app.route('/salvar_chaves', methods=['POST'])
def salvar_chaves():
    api_key = request.form.get('binance_key')
    secret_key = request.form.get('binance_secret')
    openai_key = request.form.get('openai_key')
    with open('chaves.txt', 'w') as f:
        f.write(f'BINANCE_KEY={api_key}\nBINANCE_SECRET={secret_key}\nOPENAI_KEY={openai_key}')
    return 'Chaves salvas com sucesso!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))