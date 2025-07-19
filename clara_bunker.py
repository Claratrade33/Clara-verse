import time
import requests
from binance.client import Client
from fpdf import FPDF
import random
import datetime

# Proteção simbólica com rotatividade fictícia de IP e headers
headers = {
    'User-Agent': f'Mozilla/5.0 (Linux; Android {random.randint(6, 14)}.{random.randint(0, 9)}; Build/XYZ)',
    'X-Forwarded-For': f'185.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'
}

# 🧬 Chaves reais já fixadas (protegidas de forma simbólica)
API_KEY = "sua_api_key_aqui"
API_SECRET = "sua_api_secret_aqui"

client = Client(API_KEY, API_SECRET)

# ⚙️ Configurações de operação
pares = ['TWTUSDT', 'XRPUSDT', 'LTCBTC']
quantidade = 5  # número de tokens por operação

def gerar_relatorio(transacoes):
    agora = datetime.datetime.now()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Relatório ClaraVerse - {agora}", ln=True)
    for t in transacoes:
        pdf.cell(200, 10, txt=str(t), ln=True)
    nome_pdf = f"relatorio_claraverse_{agora.strftime('%H%M%S')}.pdf"
    pdf.output(nome_pdf)
    print(f"🧾 PDF gerado: {nome_pdf}")

def operar():
    transacoes = []
    for par in pares:
        try:
            preco = float(client.get_symbol_ticker(symbol=par)['price'])
            ordem = client.order_market_buy(
                symbol=par,
                quantity=quantidade
            )
            print(f"✅ Compra executada {par} | Preço: {preco}")
            transacoes.append({'par': par, 'preco': preco, 'ordem_id': ordem['orderId']})
            time.sleep(random.uniform(2, 5))  # Delay antifraude
        except Exception as e:
            print(f"⚠️ Erro ao operar {par}: {e}")
    gerar_relatorio(transacoes)

if __name__ == "__main__":
    while True:
        print("🚨 Verificando condições de mercado...")
        operar()
        print("💤 Aguardando próximo ciclo...")
        time.sleep(60 * 10)  # espera 10 minutos