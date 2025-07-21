from flask import Flask, render_template, request, redirect, session, jsonify
from cryptography.fernet import Fernet
from datetime import timedelta
from binance.client import Client
import openai
import os, json

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(hours=6)

# Chave fixa criptográfica (pode ser gerada com Fernet.generate_key())
CHAVE_CRIPTO_FIXA = b'xApbCQFxxa3Yy3YKkzP9JkkfE4WaXxN8eSpK7uBRuGA='
fernet = Fernet(CHAVE_CRIPTO_FIXA)

# Armazenamento interno
usuarios = {'admin': 'claraverse2025'}
chaves_armazenadas = {}
saldo_simulado = 10000.00
modo_auto_ativo = False

# Rota inicial
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        if usuario in usuarios and usuarios[usuario] == senha:
            session['usuario'] = usuario
            return redirect('/painel')
        return render_template('login.html', erro='Login inválido')
    return render_template('login.html')

@app.route('/painel')
def painel():
    if 'usuario' not in session:
        return redirect('/login')
    return render_template('painel.html', saldo=saldo_simulado)

@app.route('/configurar')
def configurar():
    if 'usuario' not in session:
        return redirect('/login')
    return render_template('configurar.html')

@app.route('/salvar_chaves', methods=['POST'])
def salvar_chaves():
    try:
        data = request.form
        chaves_armazenadas['binance_key'] = fernet.encrypt(data['binance_key'].encode()).decode()
        chaves_armazenadas['binance_secret'] = fernet.encrypt(data['binance_secret'].encode()).decode()
        chaves_armazenadas['openai'] = fernet.encrypt(data['openai_key'].encode()).decode()

        with open("chaves.dat", "w") as f:
            json.dump(chaves_armazenadas, f)

        return redirect('/painel')
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/obter_preco')
def obter_preco():
    try:
        res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        preco = float(res.json()['price'])
        return jsonify({'preco': preco})
    except:
        return jsonify({'preco': 'erro'})

@app.route('/obter_saldo')
def obter_saldo():
    return jsonify({'saldo': round(saldo_simulado, 2)})

@app.route('/executar_acao', methods=['POST'])
def executar_acao():
    global saldo_simulado
    try:
        data = request.get_json()
        acao = data.get("acao")

        if acao == "entrada":
            saldo_simulado -= 100
            mensagem = "🔵 Ordem de ENTRADA executada."
        elif acao == "stop":
            saldo_simulado -= 50
            mensagem = "🔴 STOP acionado."
        elif acao == "alvo":
            saldo_simulado += 150
            mensagem = "🟢 ALVO alcançado!"
        elif acao == "automatico":
            mensagem = "🤖 Modo automático ativado."
        else:
            mensagem = "❌ Ação desconhecida."

        return jsonify({'mensagem': mensagem})
    except Exception as e:
        return jsonify({'mensagem': 'Erro ao executar ação: ' + str(e)})

@app.route('/obter_sugestao_ia', methods=['POST'])
def obter_sugestao_ia():
    try:
        if not os.path.exists("chaves.dat"):
            return jsonify({'resposta': '⚠️ Chave da OpenAI não configurada.'})

        with open("chaves.dat", "r") as f:
            chaves = json.load(f)
        openai_key = fernet.decrypt(chaves['openai'].encode()).decode()
        openai.api_key = openai_key

        prompt = request.json.get('prompt', 'Sugira uma ação de trading para o par BTC/USDT.')
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        conteudo = resposta.choices[0].message.content
        return jsonify({'resposta': conteudo})
    except Exception as e:
        return jsonify({'resposta': 'Erro: ' + str(e)})

if __name__ == '__main__':
    app.run(debug=True)