from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/preco")
def preco():
    try:
        par = request.args.get("par", "BTCUSDT")
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={par}"
        response = requests.get(url)
        data = response.json()
        return jsonify({
            "preco": float(data["lastPrice"]),
            "variacao": float(data["priceChangePercent"]),
            "volume": float(data["volume"]),
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
