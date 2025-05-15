import requests
from bs4 import BeautifulSoup
from collections import Counter

def coletar_resultados():
    url = "https://gamblingcounting.com/pt-BR/playtech-roleta-brasileira"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        elementos = soup.select(".item.item-history span")
        numeros = [int(e.text) for e in elementos if e.text.isdigit()]

        return numeros[:100]  # últimos 100 resultados
    except Exception as e:
        print("Erro ao coletar dados:", e)
        return []

def gerar_previsoes(numeros):
    if not numeros:
        return []

    contagem = Counter(numeros)
    previsoes = contagem.most_common(5)  # top 5 números mais frequentes

    return [num for num, _ in previsoes]

# Função principal
def analisar_roleta():
    ultimos_numeros = coletar_resultados()
    palpites = gerar_previsoes(ultimos_numeros)
    return palpites
