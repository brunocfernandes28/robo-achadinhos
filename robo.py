print("ROBO ACHADINHOS INICIADO 12")

import requests
from bs4 import BeautifulSoup
import random
import time
import urllib.parse

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
    "User-Agent": "Mozilla/5.0"
}

def enviar(msg):

    try:

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

        data = {
            "chat_id": CHAT_ID,
            "text": msg
        }

        requests.post(url, data=data)

        print("Mensagem enviada no Telegram")

    except Exception as e:

        print("Erro Telegram:", e)


def buscar():

    termo = random.choice(buscas)

    print("\n🔎 Buscando:", termo)

    query = urllib.parse.quote(termo)

    url = f"https://www.google.com/search?q={query}+mercado+livre&tbm=shop"

    try:

        r = requests.get(url, headers=headers, timeout=20)

        soup = BeautifulSoup(r.text, "lxml")

    except Exception as e:

        print("Erro requisição:", e)
        return


    produtos = soup.select(".sh-dgr__grid-result")

    print("Produtos encontrados:", len(produtos))

    if not produtos:
        return


    p = random.choice(produtos)

    try:

        titulo = p.select_one(".Xjkr3b").get_text(strip=True)

        preco = p.select_one(".a8Pemb").get_text(strip=True)

        link = p.select_one("a")["href"]

    except:

        return


    msg = f"""
🔥 ACHADINHO

🛍 {titulo}

💰 {preco}

🛒 https://www.google.com{link}
"""

    print("Produto:", titulo)

    enviar(msg)


while True:

    try:

        buscar()

    except Exception as e:

        print("Erro geral:", e)

    print("\n⏳ aguardando 60s...\n")

    time.sleep(60)
