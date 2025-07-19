# clara_bunker.py (versão simplificada para exibição)

from flask import Flask, render_template_string, request
app = Flask(__name__)

@app.route("/")
def sala_operacoes():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sala de Operações</title>
        <style>
            body { background: black; color: cyan; font-family: monospace; text-align: center; }
            .botao { margin: 20px; padding: 15px; background: #00ffff; color: black; border: none; border-radius: 5px; font-weight: bold; }
            .ordens { margin-top: 30px; border: 1px solid cyan; padding: 20px; border-radius: 10px; background: #111; display: inline-block; }
        </style>
    </head>
    <body>
        <h1>🧠 ClarinhaBubi na Sala de Operações</h1>
        <button class="botao">EXECUTAR ORDEM</button>
        <button class="botao">MODO AUTOMÁTICO</button>
        <div class="ordens">
            <h2>📄 Ordens Executadas:</h2>
            <div style="color: red;">Erro Automático: {"code":-2015,"msg":"Invalid API-key, IP, or permissions for action"}</div>
            <div style="color: green;">✅ Ordem simulada com sucesso! Teste de conexão passou.</div>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
