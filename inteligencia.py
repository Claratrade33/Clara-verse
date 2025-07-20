import requests
import openai

def buscar_dados_binance(par="BTCUSDT"):
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={par}"
        resposta = requests.get(url)
        dados = resposta.json()
        return {
            "preco": float(dados.get("lastPrice", 0)),
            "variacao": float(dados.get("priceChangePercent", 0)),
            "volume": float(dados.get("volume", 0))
        }
    except Exception as e:
        return {"erro": str(e)}

def detectar_lateralizacao(variacao, volume):
    if abs(variacao) < 0.3 and volume > 100:
        return True
    return False

def consultar_gpt(openai_api_key, preco, lateralizando):
    openai.api_key = openai_api_key
    mensagem = f'''
    Análise técnica BTC/USDT:
    Preço atual: {preco}
    Mercado lateralizando: {'Sim' if lateralizando else 'Não'}

    Com base nessas informações, forneça:
    1. Entrada ideal (em USDT),
    2. Alvo (take profit),
    3. Stop (stop loss),
    4. Estratégia simbólica e espiritual de vitória sobre os algoritmos da Binance.
    Retorne tudo em JSON estruturado com os campos: entrada, alvo, stop, estrategia.
    '''
    resposta = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": mensagem}]
    )
    conteudo = resposta.choices[0].message.content
    return conteudo