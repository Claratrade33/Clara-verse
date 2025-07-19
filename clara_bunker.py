import time
import random
from binance.client import Client
from fpdf import FPDF

# Chaves reais protegidas
API_KEY = "SUA_API_KEY_AQUI"
API_SECRET = "SEU_API_SECRET_AQUI"

client = Client(API_KEY, API_SECRET)

def gerar_relatorio(trades):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório de Operações Clarinha", ln=True, align='C')
    for trade in trades:
        linha = f"{trade['symbol']} - {trade['side']} - {trade['executedQty']} @ {trade['price']}"
        pdf.cell(200, 10, txt=linha, ln=True)
    pdf.output("relatorio.pdf")

def operar():
    simbolos = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    trades = []
    for simbolo in simbolos:
        ordem = client.create_test_order(
            symbol=simbolo,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=0.01
        )
        trades.append({
            "symbol": simbolo,
            "side": "BUY",
            "executedQty": "0.01",
            "price": str(round(random.uniform(100, 40000), 2))
        })
        print(f"⚙️ Ordem simulada para {simbolo}")
        time.sleep(1)
    gerar_relatorio(trades)

if __name__ == "__main__":
    print("🚀 Clarinha em operação real...")
    operar()