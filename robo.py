print("ROBO ACHADINHOS FUNCIONANDO 4.0")

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
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
"Accept": "application/json",
"Accept-Language": "pt-BR,pt;q=0.9",
"Connection": "keep-alive"
}

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
        print("Erro Telegram:", e)


def buscar():

    termo = random.choice(buscas)

    print("\n🔎 Buscando:", termo)

    url = f"https://api.mercadolibre.com/sites/MLB/search?q={termo}"

    try:

        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            print("⚠️ API bloqueou:", r.status_code)
            return

        data = r.json()

    except Exception as e:
        print("Erro requisição:", e)
        return


    if "results" not in data:
        print("⚠️ API não retornou produtos")
        return

    produtos = data["results"]

    print("Produtos encontrados:", len(produtos))

    if not produtos:
        return

    produto = random.choice(produtos)

    titulo = produto.get("title")
    preco = produto.get("price")
    link = produto.get("permalink")

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

    print("\n⏳ aguardando 15s...")

    time.sleep(15)
