print("ROBO ACHADINHOS FUNCIONANDO")

import requests
from bs4 import BeautifulSoup
import time
import random

TOKEN = "SEU_TOKEN_AQUI"
CHAT_ID = "SEU_CHAT_ID_AQUI"

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
"Accept-Language": "pt-BR,pt;q=0.9",
"Accept": "text/html"
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
    except:
        print("Erro ao enviar mensagem")


def buscar():

    termo = random.choice(buscas)

    print("\n🔎 Buscando:", termo)

    url = f"https://lista.mercadolivre.com.br/{termo.replace(' ','-')}"

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    produtos = soup.select("li.ui-search-layout__item")

    print("Produtos encontrados:", len(produtos))

    if len(produtos) == 0:
        print("⚠️ Nenhum produto encontrado")
        return

    for p in produtos[:5]:

        try:

            titulo_tag = p.select_one("h2")

            if not titulo_tag:
                continue

            titulo = titulo_tag.get_text(strip=True)

            link_tag = p.select_one("a")

            if not link_tag:
                continue

            link = link_tag["href"]

            preco_tag = p.select_one(".andes-money-amount__fraction")

            if not preco_tag:
                continue

            preco = preco_tag.get_text()

            print("Produto:", titulo)
            print("Preço:", preco)

            msg = f"""
🔥 Produto encontrado

🛍 {titulo}

💰 R${preco}

🛒 {link}
"""

            enviar(msg)

            return

        except Exception as e:

            print("Erro analisando produto:", e)


while True:

    buscar()

    print("\n⏳ aguardando 8s...")

    time.sleep(8)
