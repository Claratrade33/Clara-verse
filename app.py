from flask import Flask, render_template
from binance_handler import BinanceHandler

app = Flask(__name__)
binance = BinanceHandler()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/price")
def price():
    btc_price = binance.get_price("BTCUSDT")
    return {"BTCUSDT": btc_price}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)