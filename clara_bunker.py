import os
from flask import Flask, render_template_string, request, jsonify
from cryptography.fernet import Fernet
from binance.client import Client
from openai import OpenAI

# CHAVE FERNET USADA PARA DESCRIPTOGRAFAR
FERNET_KEY = "WS2w38PfSNFIwUDWHEZSUVaaBbC36rY0AWd_9Url870="
fernet = Fernet(FERNET_KEY.encode())

# CHAVES CRIPTOGRAFADAS
API_KEY = fernet.decrypt(b"gAAAAABofByBegKeqcSRN-lmgaanOOcM5O0Dtu7z2iYK_-suiNcRNlSiFdeInAvys66mWh1NBoiQNmqUwqZ_T-6H4e6rN5ZQRUmWuN_uhl5jb7ZfVrqVjAxXuaVSv9AMclZouDtigmvkQSLS58SSIVNhLjpjdmtX6xL9BN71bo1lsOltx5rUq8I=").decode()
API_SECRET = fernet.decrypt(b"gAAAAABofByB-BP_jDBCmDRIm5yL397B-p0w14TW8ElNTV5KAMXDY3Bd3p-Gw0N5TgwJ4wlF7URd7t1KnexICFpNX5fI9M6mfyrsCm4z1A3uDFO7DBkDdW5cR795ZDNp3tKRiQO_EE2-Xj7r-OONhYXXVHWKsaS_jOjmZR3iOtqFqzn-dEJc2I0=").decode()
OPENAI_KEY = fernet.decrypt(b"gAAAAABofByBbLcXkUQfo6P0jLJP93NXWM_kSaV-0P1UIhpxZ05I719DGuTUPHM6sFdeAFimCoSBU2RGTN8nyteMd9o3V8gZ7w==").decode()

# INICIALIZAÇÃO
app = Flask(__name__)
binance = Client(API_KEY, API_SECRET)
client_openai = OpenAI(api_key=OPENAI_KEY)

# INTERFACE VISUAL ATUALIZADA
html = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ClaraVerse | Painel de Operações</title>
    <style>
        body {
            margin: 0; padding:
