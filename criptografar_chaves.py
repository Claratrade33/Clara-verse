from cryptography.fernet import Fernet

FERNET_KEY = "0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="  # mesma usada no bunker
fernet = Fernet(FERNET_KEY.encode())

sua_api = "SUA_API_KEY_AQUI"
seu_secret = "SEU_SECRET_KEY_AQUI"

api_cript = fernet.encrypt(sua_api.encode()).decode()
secret_cript = fernet.encrypt(seu_secret.encode()).decode()

print("API_KEY_CRYPT =")
print(api_cript)
print("\nAPI_SECRET_CRYPT =")
print(secret_cript)