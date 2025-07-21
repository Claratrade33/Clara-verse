from flask import Flask, render_template, request, redirect, session, jsonify
from cryptography.fernet import Fernet
from binance.client import Client
from datetime import timedelta
import requests, openai, threading, time, os, json

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(hours=6)

CHAVE_CRIPTO_FIXA = b'xApbCQFxxa3Yy3YKkzP9JkkfE4WaXxN8eSpK7uBRuGA='
fernet = Fernet(CHAVE_CRIPTO_FIXA)

usuarios = {'admin': 'claraverse2025'}
saldo_simulado = 10000.00
modo_auto_ativo = False

# Chaves criptografadas embutidas
chaves_armazenadas = {
    "binance": "gAAAAABofh51AucJK0rK5J5A9DwHOh3b3EPL-l6s8-snYTklf_L0Ad9DVkHfHCA9rx35nSvHewI8lB3aKCqO0Sk3dUndZovo8sOEwsa0oKzkZijAaF9XvV1vNdCQQf2vJoaNZdDsyDdM7X0GJgAkDfiMTUwa9qkOGgs58nss74TX2Ejd9VeCAeE=",
    "binance_secret": "gAAAAABofh51uzzxCX2sL7ZetXoosEue7pYABue5ve6I4_t23sQU9B-dOJhLlkDc7Z_YPm0P59PhGGGCU50p-T7wCnNZhUJuQlI7GPhTFhdAcBNO_RDqJjo4ixaPebbkXK8l6EkmTdPyFQz_ANinBJ5QeGPgqtEqFWqi0TbrfmEiBZi-YoTHMTY=",
    "openai": "gAAAAABofh51Olb8C8EztOIxuEUPw6C4-r6Odj53xfdnO3VzvvGYEMAGyUPhmaxe1lDh3H_lcRun3SKW8HRBD1MNHrygbyYsCOBCjAnDU8tj_z-ZjiiF1GcOZmTAI86UOoB3ieEF06LKw8OlT44I0-wZz5k-16t-dYydvH4hyIt_jPu3ohlG3o8aBPZGyeXRolgc4SeUCiO-P3dSuNJt5UU3oxYHYsrjbPEOn85AvmGz1bsko3RfpFTXzOeG-uuXc6qaUjp5h86K1CRBiTEI32Juiy_qkxf2K0aQR5oIh5fHMzEsv21cH3g="
}

def loop_automatico():
    global modo_auto_ativo, saldo_simulado
    while modo_auto_ativo:
        try:
            print("ð¤ IA Clarinha analisando...")
            openai_key = fernet.decrypt(chaves_armazenadas['openai'].encode()).decode()
            bin_key = fernet.decrypt(chaves_armazenadas['binance'].encode()).decode()
            bin_sec = fernet.decrypt(chaves_armazenadas['binance_secret'].encode()).decode()
            from clarinha_oraculo import analisar_mercado_e_sugerir
            resposta = analisar_mercado_e_sugerir(bin_key, bin_sec, openai_key)
            conteudo = resposta.get("resposta", "").lower()
            if "comprar" in conteudo:
                saldo_simulado -= 10
                print("ð Compra simulada!")
            elif "vender" in conteudo:
                saldo_simulado += 10
                print("â¤ï¸ Venda simulada!")
            else:
                print("âª IA recomendou aguardar.")
        except Exception as e:
            print("Erro IA:", str(e))
        time.sleep(15)

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
        return render_template('login.html', erro='Credenciais invÃ¡lidas.')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return render_template('dashboard.html', saldo=saldo_simulado)
    return redirect('/login')

@app.route('/painel')
def painel():
    if 'usuario' in session:
        return render_template('painel.html', saldo=saldo_simulado)
    return redirect('/login')

@app.route('/executar_acao', methods=['POST'])
def executar_acao():
    global saldo_simulado, modo_auto_ativo
    dados = request.json
    acao = dados.get('acao')

    if acao == 'comprar':
        saldo_simulado -= 10
        return jsonify({'mensagem': 'Compra realizada (simulaÃ§Ã£o)', 'saldo': saldo_simulado})
    elif acao == 'vender':
        saldo_simulado += 10
        return jsonify({'mensagem': 'Venda realizada (simulaÃ§Ã£o)', 'saldo': saldo_simulado})
    elif acao == 'auto':
        if not modo_auto_ativo:
            modo_auto_ativo = True
            threading.Thread(target=loop_automatico).start()
            return jsonify({'mensagem': 'Modo automÃ¡tico ativado!', 'saldo': saldo_simulado})
        else:
            modo_auto_ativo = False
            return jsonify({'mensagem': 'Modo automÃ¡tico desativado!', 'saldo': saldo_simulado})
    return jsonify({'mensagem': 'AÃ§Ã£o invÃ¡lida.', 'saldo': saldo_simulado})

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

application = app

if __name__ == '__main__':
    app.run(debug=True)
