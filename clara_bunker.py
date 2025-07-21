from flask import Flask, render_template, request, redirect, session, jsonify
from cryptography.fernet import Fernet
from binance.client import Client
from datetime import timedelta
import requests, openai, threading, time, os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(hours=6)

# Chave fixa para criptografia
CHAVE_CRIPTO_FIXA = b'xApbCQFxxa3Yy3YKkzP9JkkfE4WaXxN8eSpK7uBRuGA='
fernet = Fernet(CHAVE_CRIPTO_FIXA)

usuarios = {'admin': 'claraverse2025'}
chaves_armazenadas = {}
saldo_simulado = 10000.00
modo_auto_ativo = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('usuario')
        senha = request.form.get('senha')
        if user in usuarios and usuarios[user] == senha:
            session['usuario'] = user
            return redirect('/painel')
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
        return redirect('/painel')
    except Exception as e:
        return f"Erro ao salvar as chaves: {str(e)}"

@app.route('/executar_acao', methods=['POST'])
def executar_acao():
    global saldo_simulado
    acao = request.form.get('acao')
    if acao == 'entrada':
        saldo_simulado -= 100
    elif acao == 'alvo':
        saldo_simulado += 150
    elif acao == 'stop':
        saldo_simulado -= 50
    return jsonify({'mensagem': f"Ação {acao} executada com sucesso!", 'saldo': saldo_simulado})

@app.route('/sugestao_ia', methods=['POST'])
def sugestao_ia():
    try:
        openai_key = fernet.decrypt(chaves_armazenadas['openai'].encode()).decode()
        openai.api_key = openai_key
        prompt = "Qual a melhor decisão agora para o par BTC/USDT?"
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({'resposta': resposta.choices[0].message.content})
    except Exception as e:
        return jsonify({'erro': str(e)})

@app.route('/ativar_auto', methods=['POST'])
def ativar_auto():
    global modo_auto_ativo
    modo_auto_ativo = True
    threading.Thread(target=loop_automatico).start()
    return jsonify({'mensagem': 'Modo automático ativado.'})

@app.route('/parar_auto', methods=['POST'])
def parar_auto():
    global modo_auto_ativo
    modo_auto_ativo = False
    return jsonify({'mensagem': 'Modo automático desativado.'})

def loop_automatico():
    global modo_auto_ativo, saldo_simulado
    while modo_auto_ativo:
        try:
            print("🤖 IA Clarinha analisando...")
            openai_key = fernet.decrypt(chaves_armazenadas['openai'].encode()).decode()
            openai.api_key = openai_key
            from clarinha_oraculo import analisar_mercado_e_sugerir
            resposta = analisar_mercado_e_sugerir()
            if "comprar" in resposta.lower():
                saldo_simulado -= 100
            elif "vender" in resposta.lower():
                saldo_simulado += 150
            print("💡 SUGESTÃO:", resposta)
        except Exception as e:
            print("Erro no modo automático:", e)
        time.sleep(30)

# ✅ Correção para o Render reconhecer o app
application = app