from binance.client import Client
from cryptography.fernet import Fernet

# Chave secreta usada para descriptografar a API key
fernet_key = b'OTk3HEk2fBFAiSAR4Rl-gYpV6aFsHoSLFYjGi1IOBLE='
fernet = Fernet(fernet_key)

# API key criptografada
api_key_criptografada = 'gAAAAABoex3nMGAhwxqJxOLjcBxB2RC6kaeXr2LhBNorskZir-4hN_EfBNeLyP92KtIvZtwa_xjwdAoJRfqeRbTRmjZ42TANRzv9R3sTi68fxt-WUVGnTjtTzeZdWp7-_KviMI-rED34tPxzoi0zwkyPQh2bo23m4PKpsmwycfHlzE96iDnd3xc='

# Descriptografa a API key
api_key = fernet.decrypt(api_key_criptografada.encode()).decode()

# Inicializa o client apenas com a API Key pública
client = Client(api_key, None)

# Exemplo: imprime os preços atuais dos pares de mercado
tickers = client.get_all_tickers()
for ticker in tickers[:10]:
    print(ticker)
