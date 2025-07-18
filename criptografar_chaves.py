from cryptography.fernet import Fernet

# Substitua pela mesma chave do seu bunker
FERNET_KEY = b"0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="
f = Fernet(FERNET_KEY)

# Suas chaves reais da Binance
api_key_real = b'SUA_API_KEY_AQUI'
api_secret_real = b'SUA_SECRET_KEY_AQUI'

api_key_cripto = f.encrypt(api_key_real)
api_secret_cripto = f.encrypt(api_secret_real)

print("API_KEY_CIFRADA =", api_key_cripto)
print("API_SECRET_CIFRADA =", api_secret_cripto)
