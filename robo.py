print("ROBO ACHADINHOS FUNCIONANDO 3.0")

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

def enviar(msg):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    try:
        requests.post(url, data=data, timeout=10)
        print("📨 Mensagem enviada no Telegram")
    except Exception as e:
        print("Erro ao enviar Telegram:", e)


def buscar():

    termo = random.choice(buscas)

    print("\n🔎 Buscando:", termo)

    url = f"https://api.mercadolibre.com/sites/MLB/search?q={termo}"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()
    except Exception as e:
        print("Erro na requisição:", e)
        return

    if "results" not in data:
        print("⚠️ API não retornou produtos")
        print(data)
        return

    produtos = data["results"]

    print("Produtos encontrados:", len(produtos))

    if len(produtos) == 0:
        return

    produto = random.choice(produtos)

    titulo = produto.get("title", "Produto")
    preco = produto.get("price", "0")
    link = produto.get("permalink", "")

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

    print("\n⏳ aguardando 10s...")

    time.sleep(10)
