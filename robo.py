print("ROBO ACHADINHOS INICIADO 11")

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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def enviar(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": msg
        }
        requests.post(url, data=payload, timeout=10)
        print("📨 Mensagem enviada no Telegram")
    except Exception as e:
        print("Erro Telegram:", e)

# ==============================
# MÉTODO 1 - HTML DIRETO
# ==============================
def buscar_html(termo):

    try:

        url = f"https://lista.mercadolivre.com.br/{termo.replace(' ','-')}"

        r = requests.get(url, headers=headers, timeout=15)

        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "lxml")

        produtos = soup.select("li.ui-search-layout__item, div.ui-search-result")

        if not produtos:
            return None

        p = random.choice(produtos)

        titulo = p.select_one("h2").get_text(strip=True)
        link = p.select_one("a")["href"]

        preco_tag = p.select_one(".andes-money-amount__fraction")
        preco = preco_tag.get_text() if preco_tag else "?"

        return titulo, preco, link

    except:
        return None


# ==============================
# MÉTODO 2 - PROXY ALLORIGINS
# ==============================
def buscar_proxy(termo):

    try:

        url_ml = f"https://lista.mercadolivre.com.br/{termo.replace(' ','-')}"

        proxy = "https://api.allorigins.win/raw?url=" + urllib.parse.quote(url_ml)

        r = requests.get(proxy, headers=headers, timeout=20)

        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "lxml")

        produtos = soup.select("li.ui-search-layout__item, div.ui-search-result")

        if not produtos:
            return None

        p = random.choice(produtos)

        titulo = p.select_one("h2").get_text(strip=True)
        link = p.select_one("a")["href"]

        preco_tag = p.select_one(".andes-money-amount__fraction")
        preco = preco_tag.get_text() if preco_tag else "?"

        return titulo, preco, link

    except:
        return None


# ==============================
# MÉTODO 3 - API NÃO OFICIAL
# ==============================
def buscar_api(termo):

    try:

        url = f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&limit=20"

        r = requests.get(url, timeout=15)

        if r.status_code != 200:
            return None

        data = r.json()

        resultados = data.get("results")

        if not resultados:
            return None

        p = random.choice(resultados)

        titulo = p.get("title")
        preco = p.get("price")
        link = p.get("permalink")

        return titulo, preco, link

    except:
        return None


# ==============================
# BUSCA PRINCIPAL
# ==============================
def buscar():

    termo = random.choice(buscas)

    print("\n🔎 Buscando:", termo)

    resultado = buscar_html(termo)

    if not resultado:
        print("HTML falhou, tentando proxy...")
        resultado = buscar_proxy(termo)

    if not resultado:
        print("Proxy falhou, tentando API...")
        resultado = buscar_api(termo)

    if not resultado:
        print("❌ Nenhum método encontrou produtos")
        return

    titulo, preco, link = resultado

    print("Produto:", titulo)

    msg = f"""
🔥 ACHADINHO ENCONTRADO

🛍 {titulo}

💰 R${preco}

🛒 {link}

⚡ Promoção pode acabar a qualquer momento
"""

    enviar(msg)


# ==============================
# LOOP PRINCIPAL
# ==============================
while True:

    try:

        buscar()

    except Exception as e:

        print("Erro geral:", e)

    print("\n⏳ aguardando 60s...\n")

    time.sleep(60)
