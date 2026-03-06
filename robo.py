print("ROBO ACHADINHOS V9.0 INICIADO")
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
"User-Agent": "Mozilla/5.0"
}

def enviar(msg):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    requests.post(url, data=data)


def buscar():

    termo = random.choice(buscas)

    print("\n🔎 Radar busca:", termo)

    url = f"https://lista.mercadolivre.com.br/{termo.replace(' ','-')}"

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    produtos = soup.select("li.ui-search-layout__item")

    print("Produtos encontrados:", len(produtos))

    for p in produtos[:20]:

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

            texto = p.get_text().lower()

            vendidos = 0

            if "vendidos" in texto:

                try:
                    partes = texto.split("vendidos")[0].split()
                    vendidos = int(partes[-1])
                except:
                    vendidos = 0

            print("\nProduto analisado")
            print("Título:", titulo)
            print("Preço:", preco)
            print("Vendidos:", vendidos)

            if vendidos >= 30:

                print("✅ ACHADINHO ENCONTRADO")

                msg = f"""
🔥 ACHADINHO ENCONTRADO

🛍 {titulo}

💰 R${preco}

📦 {vendidos} vendidos

🛒 {link}

⚡ Promoção pode acabar a qualquer momento
"""

                enviar(msg)

                return

            else:

                print("❌ reprovado")

        except Exception as e:

            print("Erro no produto:", e)


while True:

    buscar()

    print("\n⏳ próximo scan em 1s")

    time.sleep(1)
