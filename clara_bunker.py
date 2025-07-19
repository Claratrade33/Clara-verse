# clara_bunker.py
from flask import Flask, render_template_string, request
from binance.client import Client
from cryptography.fernet import Fernet
import openai

# Chaves embutidas e protegidas
fernet = Fernet(b'0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA=')
binance_key = fernet.decrypt(b'gAAAAABmUJ6V_GdJL7uO4bGnWj7nR6eLZJ...').decode()
binance_secret = fernet.decrypt(b'gAAAAABmUJ6ViMuP2UQOexNw0vbU0X...').decode()
openai.api_key = "sk-..."  # Chave OpenAI truncada aqui por segurança, use a sua real

client = Client(binance_key, binance_secret, testnet=True)  # Testnet ativo

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ClaraVerse | Sala de Operações</title>
    <style>
        body { background-color: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 40px; }
        input, button { padding: 10px; margin: 5px; }
        iframe { border: none; margin-top: 20px; }
        .painel { border: 1px solid #00ffcc; padding: 20px; border-radius: 8px; box-shadow: 0 0 20px #00ffcc77; }
    </style>
</head>
<body>
    <h1>🧠 Sala de Operações ClaraVerse</h1>
    <div class="painel">
        <form method="POST">
            <input type="text" name="par" placeholder="Par (ex: BTCUSDT)" required>
            <input type="text" name="valor" placeholder="Valor USDT" required>
            <button type="submit">Executar Ordem</button>
        </form>
        {% if resultado %}
            <p><strong>Resultado:</strong> {{ resultado }}</p>
        {% endif %}
    </div>
    <iframe src="https://www.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=5&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&theme=dark&style=1&timezone=Etc/UTC&withdateranges=1&hideideas=1&hidevolume=1&hidelegend=1&hide_side_toolbar=1" width="100%" height="400"></iframe>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def operar():
    resultado = ""
    if request.method == "POST":
        par = request.form["par"]
        valor = float(request.form["valor"])
        try:
            order = client.create_order(
                symbol=par.upper(),
                side="BUY",
                type="MARKET",
                quantity=round(valor / float(client.get_symbol_ticker(symbol=par.upper())["price"]), 3)
            )
            resultado = f"Ordem executada: {order['executedQty']} {par.split('USDT')[0]} comprados."
        except Exception as e:
            resultado = f"Erro ao executar: {str(e)}"
    return render_template_string(TEMPLATE, resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)