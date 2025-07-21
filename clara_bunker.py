from flask import Flask, render_template, request, redirect, session, jsonify
from cryptography.fernet import Fernet
from datetime import timedelta
import requests, openai, threading, time, os, json

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

def loop_automatico():
    global modo_auto_ativo, saldo_simulado
    while modo_auto_ativo:
        try:
            print("🤖 IA Clarinha analisando...")
            openai_key = fernet.decrypt(chaves_armazenadas['openai'].encode()).decode()
            from clarinha_cosmica import ClarinhaOraculo
            clarinha = ClarinhaOraculo(openai_key)
            dados = clarinha.consultar_mercado()
            resposta = clarinha.interpretar_como_deusa(dados)
            conteudo = resposta.lower()
            if "comprar" in conteudo:
                saldo_simulado -= 10
                print("💚 Compra simulada!")
            elif "vender" in conteudo:
                saldo_simulado += 10
                print("❤️ Venda simulada!")
            else:
                print("⚪ IA recomendou aguardar.")
        except Exception as e:
            print("Erro no modo automático:", str(e))
        time.sleep(15)

@app.route('/')
def index():
    return render_template('index.html', saldo=saldo_simulado)

@app.route('/salvar_chaves', methods=['POST'])
def salvar_chaves():
    dados = request.json
    chaves_armazenadas['openai'] = fernet.encrypt(dados['openaiKey'].encode()).decode()
    chaves_armazenadas['binance'] = fernet.encrypt(dados['binanceKey'].encode()).decode()
    chaves_armazenadas['binance_secret'] = fernet.encrypt(dados['binanceSecret'].encode()).decode()
    salvar_chaves_em_arquivo()
    return jsonify({'status': 'ok'})

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
        from clarinha_cosmica import ClarinhaOraculo
        openai_key = fernet.decrypt(chaves_armazenadas['openai'].encode()).decode()
        clarinha = ClarinhaOraculo(openai_key)
        dados = clarinha.consultar_mercado()
        sugestao = clarinha.interpretar_como_deusa(dados)
        return jsonify({'resposta': sugestao})
    except Exception as e:
        return jsonify({'resposta': f'Erro ao acessar a IA: {str(e)}'})

carregar_chaves()
application = app

if __name__ == '__main__':
    app.run(debug=True)