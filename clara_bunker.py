from flask import Flask, render_template_string, request, jsonify
from cryptography.fernet import Fernet
from binance.client import Client
from openai import OpenAI

FERNET_KEY = "QnTaKpFbUzmM3N4qNtHEmV_BQ8-1tnbM36wNqM1U9Ko="
fernet = Fernet(FERNET_KEY.encode())

API_KEY = fernet.decrypt(b'gAAAAABofDghf9eSxqpOqsQkR-iewv6KZXcA2FWZOPf1ognDx6Y8g4-vF9V8Po-z6W-ydMf_ohYx2H9Upq5bJ-m5nQxvCuvY8oGT6TN7KnAFbzpimAWcE30=').decode()
API_SECRET = fernet.decrypt(b'gAAAAABofDghGlcu9ejy3yfnr_UwSIJ7A0lh57IkMOnYFskyIwvPiI_G4h3p5k6_GXwCOv31jsLcnKwve-iHnatMZS02pumeLZYa-PtnW8PIBrxucLeuwAM=').decode()
OPENAI_KEY = fernet.decrypt(b'gAAAAABofDgh3onD_TVObo3dm7H0I3oysxYvC3-1ZVHvhw0AM4oR_ZwmaLHSVKUaoYH2Joq4ayNUsJ47QaSW65Y-mvNYImGViw70oy-XjAvK6KeDEfTH63g=').decode()

app = Flask(__name__)
binance = Client(API_KEY, API_SECRET)
client_openai = OpenAI(api_key=OPENAI_KEY)

@app.route("/")
def index():
    return "Bunker ativo com chaves protegidas."

application = app
