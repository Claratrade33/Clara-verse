from flask import Flask, render_template, request, redirect, session, jsonify
from cryptography.fernet import Fernet
from binance.client import Client
from datetime import timedelta
import requests, openai, threading, time, os, json

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(hours=6)

# Chave fixa criptográfica para persistência
CHAVE_CRIPTO_FIXA = b'xApbCQFxxa3Yy3YKkzP9JkkfE4WaXxN8eSpK7uBRuGA='
fernet = Fernet(CHAVE_CRIPTO_FIXA)

# Banco de dados em memória
usuarios = {'admin': 'claraverse2025'}
chaves_armazenadas = {}
saldo_simulado = 10000.00
modo_auto_ativo = False

# Carregar chaves salvas em arquivo (se existirem)
if os.path.exists('chaves.dat'):
    try:
        with open('chaves.dat', 'rb') as f:
            dados_criptografados = f.read()
            chaves_armazenadas = json.loads(fernet.decrypt(dados_criptografados).decode())
    except:
        chaves_armazenadas = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']
        if usuario in usuarios and usuarios[usuario] == senha:
            session['usuario'] = usuario
            return redirect('/painel')
        else:
            return 'Credenciais inválidas'
    return render_template('login.html')

@app.route('/painel')
def painel():
    if 'usuario' not in session:
        return redirect('/login')
    return render_template('painel.html', saldo=saldo_simulado)

@app.route('/configurar')
def configurar():
    return render_template('configurar.html')

@app.route('/salvar_chaves', methods=['POST'])
def salvar_chaves():
    try:
        binance_key = request.form.get('binance_api_key')
        binance_secret = request.form.get('binance_api_secret')
        openai_key = request.form.get('openai_api_key')

        chaves_armazenadas['binance'] = fernet.encrypt(binance_key.encode()).decode()
        chaves_armazenadas['binance_secret'] = fernet.encrypt(binance_secret.encode()).decode()
        chaves_armazenadas['openai'] = fernet.encrypt(openai_key.encode()).decode()

        with open('chaves.dat', 'wb') as f:
            f.write(fernet.encrypt(json.dumps(chaves_armazenadas).encode()))

        return redirect('/painel')
    except Exception as e:
        return f"Erro ao salvar as chaves: {str(e)}"

@app.route('/executar', methods=['POST'])
def executar():
    acao = request.json.get('acao')
    global saldo_simulado
    if acao == 'entrada':
        saldo_simulado -= 100
        return jsonify({'status': 'Compra simulada realizada', 'saldo': saldo_simulado})
    elif acao == 'stop':
        saldo_simulado -= 50
        return jsonify({'status': 'Stop Loss acionado', 'saldo': saldo_simulado})
    elif acao == 'alvo':
        saldo_simulado += 150
        return jsonify({'status': 'Take Profit atingido', 'saldo': saldo_simulado})
    else:
        return jsonify({'status': 'Ação desconhecida', 'saldo': saldo_simulado})

@app.route('/obter_preco')
def obter_preco():
    try:
        ticker = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT').json()
        return jsonify(ticker)
    except Exception as e:
        return jsonify({'erro': str(e)})

@app.route('/obter_sugestao')
def obter_sugestao():
    try:
        openai.api_key = fernet.decrypt(chaves_armazenadas['openai'].encode()).decode()
        resposta = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{"role": "user", "content": "Qual sua sugestão de operação para BTC/USDT agora?"}]
        )
        conteudo = resposta['choices'][0]['message']['content']
        return jsonify({'resposta': conteudo})
    except Exception as e:
        return jsonify({'resposta': f'Erro: {str(e)}'})

@app.route('/modo_automatico', methods=['POST'])
def modo_automatico():
    global modo_auto_ativo
    modo_auto_ativo = not modo_auto_ativo
    if modo_auto_ativo:
        threading.Thread(target=loop_automatico).start()
        return jsonify({'status': 'Modo automático ativado'})
    else:
        return jsonify({'status': 'Modo automático desativado'})

def loop_automatico():
    global modo_auto_ativo, saldo_simulado
    while modo_auto_ativo:
        try:
            print("🔁 IA Clarinha analisando em modo automático...")
            openai_key = fernet.decrypt(chaves_armazenadas['openai'].encode()).decode()
            openai.api_key = openai_key
            resposta = openai.ChatCompletion.create(
                model='gpt-4',
                messages=[{"role": "user", "content": "BTC vai subir ou cair agora? Responda com 'comprar', 'vender' ou 'aguardar'."}]
            )
            decisao = resposta['choices'][0]['message']['content'].lower()
            if 'comprar' in decisao:
                saldo_simulado -= 100
            elif 'vender' in decisao:
                saldo_simulado += 120
            print(f'💡 Clarinha decidiu: {decisao.upper()} | Saldo: {saldo_simulado}')
            time.sleep(15)
        except Exception as e:
            print(f'Erro no modo automático: {e}')
            modo_auto_ativo = False

# Para o Render reconhecer o app
application = app

if __name__ == '__main__':
    app.run(debug=True)