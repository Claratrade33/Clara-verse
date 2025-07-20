import openai
from binance.client import Client
import datetime
import json

class ClarinhaEstrategista:
    def __init__(self, binance_api_key, binance_api_secret, openai_api_key):
        self.client = Client(binance_api_key, binance_api_secret)
        openai.api_key = openai_api_key

    def obter_dados_mercado(self, par="BTCUSDT", intervalo="1m", limite=100):
        try:
            velas = self.client.get_klines(symbol=par, interval=intervalo, limit=limite)
            return [{
                "tempo": v[0],
                "abertura": float(v[1]),
                "maxima": float(v[2]),
                "minima": float(v[3]),
                "fechamento": float(v[4]),
                "volume": float(v[5])
            } for v in velas]
        except Exception as e:
            return {"erro": str(e)}

    def gerar_contexto_para_gpt(self, dados):
        candles = json.dumps(dados[-20:], indent=2)
        prompt = f"""
Você é a Clarinha, uma IA financeira altamente avançada com visão espiritual e lógica de mercado.

Analise os candles abaixo e responda apenas com um JSON contendo:

- "entrada": preço de entrada sugerido (ou "AGUARDAR" se não for momento ideal)
- "alvo": alvo recomendado (ponto de take profit)
- "stop": ponto de stop loss
- "confianca": valor de 0 a 100 sobre a convicção da análise
- "detectar": "laterizacao", "quebra", "alta", "queda" ou "ruido"

Candles:
{candles}
"""
        return prompt.strip()

    def analisar_com_gpt(self, dados):
        prompt = self.gerar_contexto_para_gpt(dados)
        try:
            resposta = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é uma estrategista de operações financeiras."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            conteudo = resposta['choices'][0]['message']['content']
            return json.loads(conteudo)
        except Exception as e:
            return {"erro": str(e)}

    def operar(self, par="BTCUSDT"):
        dados = self.obter_dados_mercado(par=par)
        if "erro" in dados:
            return dados
        return self.analisar_com_gpt(dados)