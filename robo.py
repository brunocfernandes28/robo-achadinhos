print("ROBO ACHADINHOS V7.0 INICIADO")
import requests
from bs4 import BeautifulSoup
import time
import random

TOKEN = "7943259231:AAGrv6bYjdGABhKrr9W2i_roYWDmCcYKIhk"
CHAT_ID = "-1003895577987"

buscas = [
"vestido feminino",
"lingerie",
"bolsa feminina",
"tenis feminino",
"chapinha cabelo",
"cafeteira",
"air fryer",
"panela antiaderente",
"carrinho bebe",
"baba eletronica",
"aspirador automotivo",
"compressor ar portatil",
"carregador veicular",
"smartwatch",
"fone bluetooth"
]

headers = {
"User-Agent":"Mozilla/5.0"
}

def enviar(msg):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
    "chat_id":CHAT_ID,
    "text":msg
    }

    requests.post(url,data=data)

def buscar():

    termo=random.choice(buscas)

    print("\n🔎 Radar busca:",termo)

    url=f"https://lista.mercadolivre.com.br/{termo.replace(' ','-')}"

    r=requests.get(url,headers=headers)

    soup=BeautifulSoup(r.text,"html.parser")

    produtos=soup.select("li.ui-search-layout__item")

    print("Produtos encontrados:",len(produtos))

    for p in produtos[:20]:

        try:

            titulo=p.select_one("h2").text.strip()

            link=p.select_one("a")["href"]

            preco=p.select_one(".andes-money-amount__fraction").text

            vendidos=p.text.lower()

            print("\nProduto analisado")
            print(titulo)

            if "vendido" in vendidos:

                print("Produto popular")

            msg=f"""
🔥 ACHADINHO ENCONTRADO

🛍 {titulo}

💰 R${preco}

🛒 {link}

⚡ Promoção pode acabar a qualquer momento
"""

            enviar(msg)

            return

        except:
            continue

while True:

    buscar()

    print("\n⏳ próximo scan em 3 minutos")

    time.sleep(180)
