
import os
from cryptography.fernet import Fernet
from binance.client import Client

# Chave secreta (protegida)
KEY = b'iLOW9XHOGVAuCDb1T9QcV6f-Cs72UOr8L5dEBfv9r1w='
fernet = Fernet(KEY)

# Dados criptografados da API (exemplo simbólico)
API_KEY_CRYPT = b'gAAAAABl...=='  # substitua pela sua versão criptografada real
API_SECRET_CRYPT = b'gAAAAABl...=='

# Descriptografar API
api_key = fernet.decrypt(API_KEY_CRYPT).decode()
api_secret = fernet.decrypt(API_SECRET_CRYPT).decode()

# Conectar à Binance
client = Client(api_key, api_secret)

# Lógica básica da Clarinha (exemplo)
def operar():
    ticker = client.get_symbol_ticker(symbol="BTCUSDT")
    print("Preço BTC/USDT:", ticker['price'])

if __name__ == "__main__":
    operar()
