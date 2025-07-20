from flask import Flask, render_template, request, redirect, url_for
from binance.client import Client
from openai import OpenAI
import os

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/painel')
def painel():
    return render_template('painel.html')

@app.route('/salvar_chaves', methods=['POST'])
def salvar_chaves():
    binance_key = request.form.get("binance_key")
    binance_secret = request.form.get("binance_secret")
    openai_key = request.form.get("openai_key")
    with open("chaves.txt", "w") as f:
        f.write(f"{binance_key}\n{binance_secret}\n{openai_key}")
    return redirect(url_for('painel'))

application = app