import time
from binance.client import Client
from cryptography.fernet import Fernet

# 🔐 Chave Fernet (blindagem simbólica SOMA)
FERNET_KEY = b"0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="
f = Fernet(FERNET_KEY)

# 🔒 Suas chaves criptografadas (modo leitura protegido)
API_KEY_CIFRADA = b"gAAAAABmZGKMG2UCQnP2C8FbCRRJ8oSoaEoL3P-B67tiCznOgSbFOP0Z99_UV1A0T4eRw9IxeBBM1v_EcV4GR_yo1M1doQLriKHfI7h-VVa6XHkgqdThQpI="
API_SECRET_CIFRADA = b"gAAAAABmZGKM3UAYOsmICu6T0VEEmVJCOId0Fh8IfDxQ5-RTBa2BZwSnqS2gYvUqBiKuybEE6t2qbRMwefJNoaM6JXo05IQ_0C5mKk-64KAh6EshukB8b4ciomr8NjZqvzoGSk1OvxwD"

# 🔓 Descriptografando
api_key = f.decrypt(API_KEY_CIFRADA).decode()
api_secret = f.decrypt(API_SECRET_CIFRADA).decode()

# 🤖 Cliente Binance (modo leitura)
client = Client(api_key, api_secret)

# 💡 Consulta de preços em tempo real
def consultar_precos():
    simbolos = ['ETHBTC', 'LTCBTC', 'BNBBTC', 'NEOBTC', 'QTUMETH']
    for simbolo in simbolos:
        try:
            ticker = client.get_symbol_ticker(symbol=symbolo)
            print(f"{simbolo}: {ticker['price']}")
        except Exception as e:
            print(f"Erro ao consultar {simbolo}: {e}")

# ⏱️ Loop principal (modo leitura contínuo)
while True:
    consultar_precos()
    time.sleep(10)