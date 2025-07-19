import time
import requests
from binance.client import Client
from cryptography.fernet import Fernet
from datetime import datetime

# Chave de criptografia usada (deve ser mantida em segurança e fora do código em produção)
secret_key = b'8sCruBG2_Jh5Rp_IwGN20hCn5rMSEXVwr5i--0x75VA='

fernet = Fernet(secret_key)

# Chaves criptografadas (exemplo)
API_KEY_CRYPT = "gAAAAABoexeM1eIBMsoYoDj8UXXi2-t5DmEJALhSq4lSF2lgOYBjYtScJV11fwspsPXAPdcP9UR_NeBUPDNHf5dg2IfQzfxHLTDzQ-Dw8Gg9jIVX28SfH2s="
API_SECRET_CRYPT = "gAAAAABoexeMs5_C-yTLeLfD61Y8x4xoqAqH6l-El3GHgqJbL9gaq3kaqvXPwpa59zG5K4K6LiQgK9ErDwvSFsxEVfAzdEVJDNZpTHBmkvTy9K5S4Bkxu04="

# Descriptografando as chaves
API_KEY = fernet.decrypt(API_KEY_CRYPT.encode()).decode()
API_SECRET = fernet.decrypt(API_SECRET_CRYPT.encode()).decode()

# Cliente Binance
client = Client(API_KEY, API_SECRET)

# Par de trading
symbol = "BTCUSDT"
quantity = 0.0001  # Exemplo

def operar():
    print("Verificando o preço atual...")
    price = float(client.get_symbol_ticker(symbol=symbol)["price"])
    print(f"Preço atual: {price}")

    print("Enviando ordem de teste de compra (modo segurança)...")
    order = client.create_test_order(
        symbol=symbol,
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quantity=quantity
    )
    print("Ordem enviada (simulada com sucesso).")

if __name__ == "__main__":
    print("Iniciando Bunker da Clarinha...")
    while True:
        try:
            operar()
            time.sleep(60)  # Espera 1 minuto entre as operações simuladas
        except Exception as e:
            print("Erro:", e)
            time.sleep(120)
