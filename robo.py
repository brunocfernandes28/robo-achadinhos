print("ROBO ACHADINHOS FUNCIONANDO RSS")

import requests
import random
import time
import xml.etree.ElementTree as ET

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
        requests.post(url, data=data)
        print("📨 Mensagem enviada no Telegram")
    except Exception as e:
        print("Erro Telegram:", e)


def buscar():

    termo = random.choice(buscas)

    print("\n🔎 Buscando:", termo)

    url = f"https://www.mercadolivre.com.br/rss/search?q={termo}"

    try:

        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            print("Erro HTTP:", r.status_code)
            return

        root = ET.fromstring(r.content)

    except Exception as e:
        print("Erro requisição:", e)
        return


    itens = root.findall(".//item")

    print("Produtos encontrados:", len(itens))

    if not itens:
        return


    item = random.choice(itens)

    titulo = item.find("title").text
    link = item.find("link").text


    msg = f"""
🔥 ACHADINHO

🛍 {titulo}

🛒 {link}
"""

    enviar(msg)


while True:

    buscar()

    print("\n⏳ aguardando 60s...\n")

    time.sleep(60)
