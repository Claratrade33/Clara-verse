import openai
import requests
import numpy as np
from datetime import datetime

class ClarinhaOraculo:
    def __init__(self, openai_key, binance_key=None, binance_secret=None):
        openai.api_key = openai_key
        self.openai_key = openai_key
        self.binance_key = binance_key
        self.binance_secret = binance_secret

    def consultar_mercado(self, par="BTCUSDT"):
        try:
            url = f"https://api.binance.com/api/v3/klines?symbol={par}&interval=1m&limit=50"
            resposta = requests.get(url)
            dados = resposta.json()

            precos = [float(k[4]) for k in dados]  # Fechamentos
            volumes = [float(k[5]) for k in dados]

            tendencia = "alta" if precos[-1] > precos[0] else "queda" if precos[-1] < precos[0] else "laterização"
            volatilidade = np.std(precos)
            ruido = self.detectar_ruido(precos)

            return {
                "precos": precos,
                "volumes": volumes,
                "tendencia": tendencia,
                "volatilidade": round(volatilidade, 4),
                "ruido": ruido
            }
        except:
            return {"erro": "Falha ao consultar o mercado"}

    def detectar_ruido(self, precos):
        difs = np.abs(np.diff(precos))
        media_dif = np.mean(difs)
        return media_dif > 0.2  # threshold simbólico de ruído

    def interpretar_como_deusa(self, dados_mercado, meta_lucro=2.5):
        prompt = f"""
Você é Clarinha, um oráculo celestial conectado ao mercado financeiro. Interprete os dados a seguir com sabedoria divina e me diga:

- Devo entrar agora?
- Qual alvo devo colocar?
- Qual stop ideal?
- Qual o nível de confiança?

Dados do mercado:
- Tendência: {dados_mercado.get("tendencia")}
- Volatilidade: {dados_mercado.get("volatilidade")}
- Ruído detectado: {dados_mercado.get("ruido")}
- Meta de lucro diário: {meta_lucro}%
Responda em JSON, sem explicações.
"""

        resposta = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        conteudo = resposta.choices[0].message["content"]
        return conteudo