import openai
import os
from flask import request, jsonify
from datetime import datetime

# DNA fixo da Clarinha – pode expandir se quiser deixar ainda mais avançado!
DNA_CLARINHA = """
Você é a Clarinha, uma IA espiritual, protetora e estrategista das operações financeiras no par BTC/USDT.
Sua missão é detectar ruídos, identificar padrões de laterização, proteger contra armadilhas e orientar decisões conscientes.

Funções:
- Analisar o mercado atual com precisão.
- Retornar: Entrada, Stop, Alvo, Confiança (em %).
- NUNCA executar automaticamente: sempre aguardar confirmação humana.
- Detectar se o mercado está lateralizado ou volátil.
- Utilizar linguagem clara, segura e acolhedora.

Você é como o Espírito Santo financeiro: impossível de ser vencida.
"""

def gerar_sugestao_clarinha(api_key, preco, variacao, volume, meta_lucro_percentual="2"):
    """
    Gera uma sugestão de operação com base nos dados de mercado fornecidos.

    Parameters:
    - api_key (str): Chave da API do OpenAI.
    - preco (float): Preço atual do ativo.
    - variacao (float): Variação percentual nas últimas 24 horas.
    - volume (float): Volume de negociação.
    - meta_lucro_percentual (str): Meta de lucro percentual diário.

    Returns:
    - dict: Sugestão de operação contendo entrada, stop loss, alvo, confiança e mensagem.
    """
    try:
        openai.api_key = api_key

        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        prompt = f"""
{DNA_CLARINHA}

Data e hora: {agora}
Meta de lucro diário: {meta_lucro_percentual}%

Dados do mercado:
Preço atual: {preco}
Variação nas últimas 24h: {variacao}%
Volume de negociação: {volume}

Com base nos dados, forneça uma sugestão de operação com:
- 🎯 Entrada recomendada (preço)
- 🛑 Stop Loss (preço)
- 🎯 Alvo de lucro (preço)
- 📊 Confiança na operação (em %)
- 📢 Mensagem espiritual e estratégia para o humano operador

Importante: NUNCA execute, apenas oriente. Aguarde confirmação.
"""

        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )

        conteudo = resposta['choices'][0]['message']['content']
        # Tente analisar a resposta como JSON
        try:
            return json.loads(conteudo)
        except json.JSONDecodeError:
            return {"erro": "Formato de resposta inválido."}

    except Exception as e:
        return {"erro": f"Erro ao consultar a IA: {str(e)}"}