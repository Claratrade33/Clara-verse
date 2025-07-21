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

# -------------------- FUNÇÃO AUTOMÁTICA --------------------
def loop_automatico():
    global modo_auto_ativo, saldo_simulado
    while modo_auto_ativo:
        try:
            print("🤖 IA Clarinha analisando...")

            # Recupera as chaves
            openai_key = fernet.decrypt(chaves_armazenadas['openai'].encode()).decode()
            bin_key = fernet.decrypt(chaves_armazenadas['binance'].encode()).decode()
            bin_sec = fernet.decrypt(chaves_armazenadas['binance_secret'].encode()).decode()

            # Roda o oráculo
            from inteligencia import analisar_mercado_e_sugerir
            resposta = analisar_mercado_e_sugerir(bin_key, bin_sec, openai_key)
            conteudo = resposta.get("resposta", "").lower()

            # Simula entrada
            if "comprar" in conteudo:
                saldo_simulado -= 10
                print("💚 Compra simulada!")
            elif "vender" in conteudo:
                saldo_simulado += 10
                print("❤️ Venda simulada!")
            else:
                print("⚪ IA recomendou aguardar.")
        except Exception as e:
            print("Erro IA:", str(e))
        time.sleep(15)

# -------------------- ROTAS --------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario in usuarios and usuarios[usuario] == senha:
            session['usuario'] = usuario
            session.permanent = True
            return redirect('/painel')
        return render_template('login.html', erro='Credenciais inválidas.')
    return render_template('login.html')

@app.route('/painel')
def painel():
    if 'usuario' in session:
        return render_template('painel.html', saldo=saldo_simulado)
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return render_template('dashboard.html', saldo=saldo_simulado)
    return redirect('/login')

@app.route('/configurar')
def configurar():
    if 'usuario' in session:
        return render_template('configurar.html')
    return redirect('/login')

@app.route('/salvar_chaves', methods=['POST'])
def salvar_chaves():
    dados = request.json
    try:
        chaves_armazenadas['openai'] = fernet.encrypt(dados['openaiKey'].encode()).decode()
        chaves_armazenadas['binance'] = fernet.encrypt(dados['binanceKey'].encode()).decode()
        chaves_armazenadas['binance_secret'] = fernet.encrypt(dados['binanceSecret'].encode()).decode()
        print("🔐 Chaves salvas com sucesso.")
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'erro', 'detalhe': str(e)})

@app.route('/executar_acao', methods=['POST'])
def executar_acao():
    global saldo_simulado, modo_auto_ativo
    dados = request.json
    acao = dados.get('acao')

    if acao == 'comprar':
        saldo_simulado -= 10
        return jsonify({'mensagem': 'Compra realizada (simulação)', 'saldo': saldo_simulado})
    elif acao == 'vender':
        saldo_simulado += 10
        return jsonify({'mensagem': 'Venda realizada (simulação)', 'saldo': saldo_simulado})
    elif acao == 'auto':
        if not modo_auto_ativo:
            modo_auto_ativo = True
            threading.Thread(target=loop_automatico).start()
            return jsonify({'mensagem': 'Modo automático ativado!', 'saldo': saldo_simulado})
        else:
            modo_auto_ativo = False
            return jsonify({'mensagem': 'Modo automático desativado!', 'saldo': saldo_simulado})
    return jsonify({'mensagem': 'Ação inválida.', 'saldo': saldo_simulado})

@app.route('/obter_saldo')
def obter_saldo():
    return jsonify({'saldo': round(saldo_simulado, 2)})

@app.route('/obter_preco')
def obter_preco():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        preco = float(r.json()['price'])
        return jsonify({'preco': preco})
    except:
        return jsonify({'preco': '--'})

@app.route('/obter_sugestao_ia')
def obter_sugestao_ia():
    try:
        from clarinha_oraculo import ClarinhaOraculo

        openai_key = fernet.decrypt(chaves_armazenadas['openai'].encode()).decode()
        clarinha = ClarinhaOraculo(openai_key)
        dados = clarinha.consultar_mercado()
        sugestao = clarinha.interpretar_como_deusa(dados)
        return jsonify({'resposta': sugestao})
    except Exception as e:
        return jsonify({'resposta': f'❌ Erro ao acessar a IA: {str(e)}'})

# -------------------- DEPLOY --------------------
application = app

if __name__ == '__main__':
    app.run(debug=True)
