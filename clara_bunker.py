import os
import time
import hmac
import hashlib
import requests
import base64
from urllib.parse import urlencode

# ================= CONFIGURAÇÕES =================

API_KEY = "Dja8iu8fmP34qAr8Tvh4VNsWo4GYbahCNxvDadvwfGCJTx3qP1JST9jBfteGPOdV"
API_SECRET = "vwWP2lnNHNWKSMNCL7mLURIeJ29fCfjFOBZON9dvzLFMsp6XGjeLaDWsWKwfknc2"
BASE_URL = "https://api.binance.com"

SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT", "PEPEUSDT",
    "DOGEUSDT", "SHIBUSDT", "LINKUSDT", "SOLUSDT", "OPUSDT", "SUIUSDT",
    "FLOKIUSDT", "1000SATSUSDT"
]

# ================= FUNÇÕES =================

def create_signature(query_string):
    return hmac.new(API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def send_signed_request(http_method, url_path, payload={}):
    timestamp = int(time.time() * 1000)
    payload.update({"timestamp": timestamp})
    query_string = urlencode(payload, True)
    signature = create_signature(query_string)
    headers = {"X-MBX-APIKEY": API_KEY}
    url = f"{BASE_URL}{url_path}?{query_string}&signature={signature}"
    response = requests.request(http_method, url, headers=headers)
    return response.json()

def get_price(symbol):
    url = f"{BASE_URL}/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    return float(response.json()['price'])

def place_order(symbol, side, quantity):
    payload = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity
    }
    return send_signed_request("POST", "/api/v3/order", payload)

# ================= LÓGICA DE OPERAÇÃO =================

def operate(symbol):
    try:
        price = get_price(symbol)
        print(f"[{symbol}] Preço atual: {price}")
        if price % 1 < 0.1:
            print(f"⚡ Comprando {symbol}")
            result = place_order(symbol, "BUY", 5)
            print(result)
        elif price % 1 > 0.9:
            print(f"⚡ Vendendo {symbol}")
            result = place_order(symbol, "SELL", 5)
            print(result)
    except Exception as e:
        print(f"[{symbol}] Erro: {e}")

# ================= LOOP DE MONITORAMENTO =================

print("🚀 Clarinha iniciou operação em modo real.")
while True:
    for symbol in SYMBOLS:
        operate(symbol)
        time.sleep(1)
    time.sleep(5)