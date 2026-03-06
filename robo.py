print("ROBO ACHADINHOS FUNCIONANDO 6.0")

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
        requests.post(url, data=data, timeout=10)
        print("📨 Mensagem enviada no Telegram")
    except Exception as e:
        print("Erro Telegram:", e)


def buscar_polycard(termo):

    try:

        url = f"https://www.mercadolivre.com.br/polycard/search?query={termo}"

        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            print("Polycard falhou:", r.status_code)
            return None

        data = r.json()

        if "results" not in data:
            return None

        return data["results"]

    except:
        return None


def buscar_api(termo):

    try:

        url = f"https://api.mercadolibre.com/sites/MLB/search?q={termo}"

        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            print("API bloqueou:", r.status_code)
            return None

        data = r.json()

        if "results" not in data:
            return None

        return data["results"]

    except:
        return None


def buscar():

    termo = random.choice(buscas)

    print("\n🔎 Buscando:", termo)

    produtos = buscar_polycard(termo)

    if not produtos:

        print("Polycard falhou, tentando API...")

        produtos = buscar_api(termo)

    if not produtos:

        print("❌ Nenhum produto encontrado")
        return

    print("Produtos encontrados:", len(produtos))

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

    print("\n⏳ aguardando 25s...")

    time.sleep(25)
