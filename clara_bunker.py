from flask import Flask, render_template, request, redirect, session, jsonify
from cryptography.fernet import Fernet
import os, requests, openai

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Chave fixa para manter a criptografia entre deploys
CHAVE_CRIPTO_FIXA = b'xApbCQFxxa3Yy3YKkzP9JkkfE4WaXxN8eSpK7uBRuGA='
fernet = Fernet(CHAVE_CRIPTO_FIXA)

# Simulação de banco de dados simples em memória
usuarios = {'admin': 'claraverse2025'}
chaves_armazenadas = {}  # Formato: {'openai': ..., 'binance': ...}
saldo_simulado = 1000.0  # Saldo inicial fictício

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario in usuarios and usuarios[usuario] == senha:
            session['usuario'] = usuario
            return redirect('/painel')
        else:
            return render_template('login.html', erro='Credenciais inválidas.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return render_template('dashboard.html')
    return redirect('/login')

@app.route('/configurar')
def configurar():
    if 'usuario' in session:
        return render_template('configurar.html')
    return redirect('/login')

@app.route('/painel')
def painel():
    if 'usuario' in session:
        return render_template('painel.html', saldo=saldo_simulado)
    return redirect('/login')

@app.route('/salvar_chaves', methods=['POST'])
def salvar_chaves():
    dados = request.json
    openai_key = dados.get('openaiKey', '')
    binance_key = dados.get('binanceKey', '')
    binance_secret = dados.get('binanceSecret', '')

    chaves_armazenadas['openai'] = fernet.encrypt(openai_key.encode()).decode()
    chaves_armazenadas['binance'] = fernet.encrypt(binance_key.encode()).decode()
    chaves_armazenadas['binance_secret'] = fernet.encrypt(binance_secret.encode()).decode()
    return jsonify({'status': 'ok', 'mensagem': 'Chaves salvas com sucesso!'})

@app.route('/executar_acao', methods=['POST'])
def executar_acao():
    global saldo_simulado
    dados = request.json
    acao = dados.get('acao')

    if acao == 'entrada':
        saldo_simulado -= 10
        return jsonify({'mensagem': 'ENTRADA realizada com sucesso.', 'saldo': saldo_simulado})
    elif acao == 'stop':
        saldo_simulado -= 5
        return jsonify({'mensagem': 'STOP acionado.', 'saldo': saldo_simulado})
    elif acao == 'alvo':
        saldo_simulado += 15
        return jsonify({'mensagem': 'ALVO atingido com lucro!', 'saldo': saldo_simulado})
    elif acao == 'auto':
        return jsonify({'mensagem': 'Modo automático ativado!', 'saldo': saldo_simulado})
    elif acao == 'executar':
        saldo_simulado -= 7
        return jsonify({'mensagem': 'Operação executada com sucesso.', 'saldo': saldo_simulado})
    else:
        return jsonify({'mensagem': 'Ação inválida.', 'saldo': saldo_simulado})

@app.route('/obter_saldo')
def obter_saldo():
    return jsonify({'saldo': saldo_simulado})

@app.route('/obter_sugestao_ia')
def obter_sugestao_ia():
    try:
        openai_key = fernet.decrypt(chaves_armazenadas['openai'].encode()).decode()
        openai.api_key = openai_key

        mensagem_sistema = "Você é uma IA financeira que sugere operações com base no mercado BTC/USDT."
        mensagem_usuario = "Qual a melhor sugestão para operar agora?"

        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": mensagem_sistema},
                {"role": "user", "content": mensagem_usuario}
            ],
            temperature=0.7
        )
        texto = resposta['choices'][0]['message']['content']
        return jsonify({'resposta': texto})
    except Exception as e:
        return jsonify({'resposta': 'IA indisponível no momento.'})

@app.route('/obter_preco')
def obter_preco():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        resposta = requests.get(url)
        preco = resposta.json()['price']
        return jsonify({'preco': preco})
    except:
        return jsonify({'preco': 'Erro'})

if __name__ == '__main__':
    app.run(debug=True)