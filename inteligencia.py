import openai
import requests

def analisar_mercado_e_sugerir(binance_api_key, binance_api_secret, openai_api_key, meta_lucro=2.5):
    openai.api_key = openai_api_key

    try:
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=15m&limit=50"
        response = requests.get(url)
        candles = response.json()

        closes = [float(c[4]) for c in candles]
        variacao = (closes[-1] - closes[-2]) / closes[-2] * 100
        tendencia = "alta" if variacao > 0 else "queda"

        prompt = f"""
        Você é uma inteligência financeira espiritualizada.
        O mercado de BTC/USDT está em {tendencia} com variação recente de {variacao:.2f}%.
        Meta de lucro diária: {meta_lucro}%.

        Sugira uma operação com:
        - Ponto de ENTRADA
        - Alvo de lucro (ALVO)
        - Stop Loss (STOP)
        - Confiança da operação (0-100%)
        """

        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        conteudo = resposta.choices[0].message.content.strip()

        return {
            "resposta": conteudo,
            "entrada": "⚡ Definida pela IA",
            "alvo": "🎯 Alvo estratégico",
            "stop": "🛑 Stop preventivo",
            "confianca": "🌟 Alta"
        }

    except Exception as e:
        return {"erro": str(e)}