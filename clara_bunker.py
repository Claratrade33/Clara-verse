from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# Templates HTML embutidos
fachada_html = '''
<!DOCTYPE html>
<html>
<head><title>ClaraVerse | Embarque</title></head>
<body style="background-color:black;color:white;text-align:center;">
    <h1>🚀 ClaraVerse - Plataforma de Operações</h1>
    <a href="/sala-operacoes"><button>EMBARCAR NA NAVE</button></a>
</body>
</html>
'''

sala_operacoes_html = '''
<!DOCTYPE html>
<html>
<head><title>Sala de Operações</title></head>
<body style="background:#111;color:#0f0;font-family:sans-serif;">
    <h2>🚀 Sala de Operações da ClarinhaBubi</h2>
    <p>Par: BTCUSDT | Preço: <span id="preco">{{ preco }}</span></p>
    <form action="/executar-ordem" method="post">
        <button type="submit">Executar Ordem</button>
    </form>
    <form action="/ativar-automatico" method="post">
        <button type="submit">Modo Automático</button>
    </form>
</body>
</html>
'''

@app.route("/")
def fachada():
    return render_template_string(fachada_html)

@app.route("/sala-operacoes")
def sala_operacoes():
    preco = round(random.uniform(116000, 118000), 2)
    return render_template_string(sala_operacoes_html, preco=preco)

@app.route("/executar-ordem", methods=["POST"])
def executar_ordem():
    return jsonify({"status": "Ordem executada", "moeda": "BTCUSDT", "preco": round(random.uniform(116000, 118000), 2)})

@app.route("/ativar-automatico", methods=["POST"])
def ativar_auto():
    return jsonify({"status": "Modo automático ativado", "ia": "ClarinhaBubi"})

if __name__ == "__main__":
    app.run()