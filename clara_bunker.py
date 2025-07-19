import os
from flask import Flask, jsonify
from cryptography.fernet import Fernet
import openai
from binance.client import Client

FERNET_KEY = "0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="
API_KEY_CRIPTO = "gAAAAABoe-lVkb4Fe4mtCIsSGJjnDPmyMrHQL7UzBkYkqyHNMiuhYIs2SfPfRp8ttfHH9m5oIxue0vcpveaRO5h-nhyre-wXpvyTQXW2JepV9hekdezGNBY="
API_SECRET_CRIPTO = "gAAAAABoe-lVRsUVMvBav37BXuB29YtzQMJWI6xitP0hD0dEnXqh6LZc7ChX2-9roWX99QUshdxKrFzbf7mms7vexBet2iRZo84yQsfkB3u9IJVGGR68MOs="
OPENAI_KEY_CRIPTO = "gAAAAABoe-lVnBTnP8heHDIdQPlk5B2i0Wdookgfr05E4F1vcVpD-HhrfQn2pXB41fYLnbLh255E3cvG1c-ZoV2HOZQ7FTI_cBETO1S8opN8bjjWXn-sJFJCMkJSklhlaDoDUuVhVYHB"

fernet = Fernet(FERNET_KEY.encode())

try:
    API_KEY = fernet.decrypt(API_KEY_CRIPTO.encode()).decode()
    API_SECRET = fernet.decrypt(API_SECRET_CRIPTO.encode()).decode()
    OPENAI_KEY = fernet.decrypt(OPENAI_KEY_CRIPTO.encode()).decode()
except Exception as e:
    raise Exception(f"Erro ao descriptografar as chaves: {str(e)}")

openai.api_key = OPENAI_KEY
binance_client = Client(API_KEY, API_SECRET)

app = Flask(__name__)

@app.route("/")
def home():
    return "ð ClaraBunker Online"

@app.route("/entrada")
def entrada():
    return jsonify({"entrada": "BTCUSDT", "alvo": "68000", "stop": "66000", "confianÃ§a": "92%"})

application = app