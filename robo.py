print("ROBO ACHADINHOS FUNCIONANDO 8.0")

import requests
from bs4 import BeautifulSoup
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
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
"Accept-Language": "pt-BR,pt;q=0.9"
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

    url = f"https://lista.mercadolivre.com.br/{termo.replace(' ','-')}"

    try:

        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            print("Erro HTTP:", r.status_code)
            return

        soup = BeautifulSoup(r.text, "html.parser")

    except Exception as e:
        print("Erro requisição:", e)
        return


    produtos = soup.select("li.ui-search-layout__item")

    print("Produtos encontrados:", len(produtos))

    if len(produtos) == 0:
        return


    p = random.choice(produtos)

    try:

        titulo = p.select_one("h2").get_text(strip=True)

        link = p.select_one("a")["href"]

        preco = p.select_one(".andes-money-amount__fraction").get_text()

    except:
        return


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

    print("\n⏳ aguardando 30s...")

    time.sleep(30)
