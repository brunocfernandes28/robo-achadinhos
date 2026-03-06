print("ROBO ACHADINHOS V6.1 INICIADO")
import requests
import time
import random

TOKEN = "7943259231:AAGrv6bYjdGABhKrr9W2i_roYWDmCcYKIhk"
CHAT_ID = "-1003895577987"

headers = {
"User-Agent":"Mozilla/5.0"
}

categorias = [
"MLB1430",
"MLB1246",
"MLB1055",
"MLB1384",
"MLB1000",
"MLB1743"
]

def enviar_telegram(msg):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
    "chat_id":CHAT_ID,
    "text":msg
    }

    requests.post(url,data=data)

def calcular_desconto(preco, antigo):

    if antigo is None:
        return 0

    try:
        return int((antigo-preco)/antigo*100)
    except:
        return 0

def buscar():

    categoria = random.choice(categorias)

    print("\n🔎 Radar categoria:",categoria)

    url=f"https://api.mercadolibre.com/sites/MLB/search?category={categoria}&limit=50"

    r=requests.get(url,headers=headers)

    data=r.json()

    produtos=data.get("results",[])

    print("Produtos encontrados:",len(produtos))

    for p in produtos:

        try:

            titulo=p["title"]
            preco=p["price"]
            antigo=p.get("original_price")
            vendidos=p["sold_quantity"]
            link=p["permalink"]

            desconto=calcular_desconto(preco,antigo)

            print("\nProduto analisado")
            print("Titulo:",titulo)
            print("Desconto:",desconto)
            print("Vendidos:",vendidos)

            if desconto>=30 and vendidos>=20:

                print("✅ ACHADINHO ENCONTRADO")

                msg=f"""
🔥 ACHADINHO ENCONTRADO

🛍 {titulo}

💰 De: R${antigo}
💸 Por: R${preco}

🔥 {desconto}% OFF
📦 {vendidos} vendidos

🛒 {link}

⚡ Promoção pode acabar a qualquer momento
"""

                enviar_telegram(msg)

                return

            else:

                print("❌ reprovado")

        except:
            continue

while True:

    buscar()

    print("\n⏳ próximo scan em 3 minutos")

    time.sleep(180)
