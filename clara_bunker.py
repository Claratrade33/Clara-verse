import os
import time
from binance.client import Client
from cryptography.fernet import Fernet

# Chave secreta (criptografada)
API_KEY_CRYPT = b'gAAAAABlZ...=='
API_SECRET_CRYPT = b'gAAAAABlZ...=='

# Descriptografar (exemplo simbólico)
fernet = Fernet(os.environ.get('CLAVE'))
api_key = fernet.decrypt(API_KEY_CRYPT).decode()
api_secret = fernet.decrypt(API_SECRET_CRYPT).decode()

client = Client(api_key, api_secret)

# Operação básica
while True:
    try:
        depth = client.get_order_book(symbol='BTCUSDT', limit=5)
        bids = depth['bids']
        asks = depth['asks']
        print("Top Bid:", bids[0], "Top Ask:", asks[0])
        time.sleep(5)
    except Exception as e:
        print("Erro:", e)
