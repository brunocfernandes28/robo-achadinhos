print("ROBO ACHADINHOS FUNCIONANDO 5.0")

import requests
import time
import random

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

headers = {
"User-Agent": "Mozilla/5.0",
"Accept": "application/json"
}

def enviar(msg):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    try:
        requests.post(url, data=data)
        print("📨 Mensagem enviada no Telegram")
    except Exception as e:
        print("Erro Telegram:", e)


def buscar():

    termo = random.choice(buscas)

    print("\n🔎 Buscando:", termo)

    url = f"https://www.mercadolivre.com.br/jm/search?q={termo}"

    try:

        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            print("Erro HTTP:", r.status_code)
            return

        data = r.json()

    except Exception as e:
        print("Erro requisição:", e)
        return


    if "results" not in data:
        print("Nenhum resultado")
        return

    produtos = data["results"]

    print("Produtos encontrados:", len(produtos))

    produto = random.choice(produtos)

    titulo = produto["title"]
    preco = produto["price"]
    link = produto["permalink"]

    print("Produto:", titulo)
    print("Preço:", preco)

    msg = f"""
🔥 ACHADINHO ENCONTRADO

🛍 {titulo}

💰 R${preco}

🛒 {link}

⚡ Promoção pode acabar a qualquer momento
"""

    enviar(msg)


while True:

    buscar()

    print("\n⏳ aguardando 20s...")

    time.sleep(20)
