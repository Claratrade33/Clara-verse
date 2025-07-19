from cryptography.fernet import Fernet

FERNET_KEY = "0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="
fernet = Fernet(FERNET_KEY.encode())

sua_api = "Yih4************XgKi"
seu_secret = "1nK************5uwz"
sua_openai = "sk-LcT3*************Ntbw7fBlbkFqrxQh6KOA64O3O3"

api_cript = fernet.encrypt(sua_api.encode()).decode()
secret_cript = fernet.encrypt(seu_secret.encode()).decode()
openai_cript = fernet.encrypt(sua_openai.encode()).decode()

print("API_KEY_CRYPT =", api_cript)
print("API_SECRET_CRYPT =", secret_cript)
print("OPENAI_KEY_CRYPT =", openai_cript)
