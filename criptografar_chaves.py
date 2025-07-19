from cryptography.fernet import Fernet

# Mesma chave usada no bunker
FERNET_KEY = "0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="
fernet = Fernet(FERNET_KEY.encode())

# Substitua com suas chaves reais aqui para criptografar novamente
openai_key = input("Digite sua chave OPENAI: ")
binance_key = input("Digite sua API KEY Binance: ")
binance_secret = input("Digite sua SECRET Binance: ")

encrypted_openai = fernet.encrypt(openai_key.encode()).decode()
encrypted_binance_key = fernet.encrypt(binance_key.encode()).decode()
encrypted_binance_secret = fernet.encrypt(binance_secret.encode()).decode()

print("\nCole no Render (.env):\n")
print(f"OPEN={encrypted_openai}")
print(f"Bia={encrypted_binance_key}")
print(f"Bia1={encrypted_binance_secret}")