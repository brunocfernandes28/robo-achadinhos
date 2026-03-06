print("ROBO ACHADINHOS FUNCIONANDO 9.0")

import requests
import random
import time

TOKEN = "7943259231:AAGrv6bYjdGABhKrr9W2i_roYWDmCcYKIhk"
CHAT_ID = "-1003895577987"

buscas = [
"smartwatch",
"fone bluetooth",
"chapinha cabelo",
"bolsa feminina",
"air fryer",
"cafeteira",
"tenis feminino"
]

def enviar(msg):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    try:
        requests.post(url, data=payload, timeout=10)
        print("Mensagem enviada no Telegram")
    except Exception as e:
        print("Erro Telegram:", e)


def buscar():

    termo = random.choice(buscas)

    print("\nBuscando:", termo)

    url = "https://api.mercadolibre.com/sites/MLB/search"

    params = {
        "q": termo,
        "limit": 20
    }

    try:

        r = requests.get(url, params=params, timeout=10)

        if r.status_code != 200:
            print("Erro HTTP:", r.status_code)
            return

        data = r.json()

    except Exception as e:
        print("Erro requisição:", e)
        return


    produtos = data.get("results", [])

    print("Produtos encontrados:", len(produtos))

    if not produtos:
        return


    produto = random.choice(produtos)

    titulo = produto.get("title")
    preco = produto.get("price")
    link = produto.get("permalink")

    msg = f"""
🔥 ACHADINHO

🛍 {titulo}

💰 R${preco}

🛒 {link}
"""

    enviar(msg)


while True:

    buscar()

    print("\nAguardando 60s...\n")

    time.sleep(60)
