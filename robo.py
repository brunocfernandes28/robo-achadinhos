import requests
from bs4 import BeautifulSoup
import time
import re
import os

TOKEN = "SEU_TOKEN_TELEGRAM"
CHAT_ID = "-1003895577987"

buscas = [

"vestido feminino","lingerie","bolsa feminina","tenis feminino","tenis masculino",
"chapinha cabelo","escova secadora","secador cabelo","depilador eletrico",
"utensilios cozinha","panela antiaderente","organizador cozinha","air fryer",
"cafeteira eletrica","carrinho bebe","baba eletronica","bolsa maternidade",
"cadeirinha bebe carro","brinquedo educativo bebe","aspirador automotivo",
"compressor ar portatil","camera veicular","carregador veicular",
"kit limpeza automotiva","fone bluetooth","smartwatch",
"caixa som bluetooth","power bank","suporte celular carro"

]

headers = {"User-Agent": "Mozilla/5.0"}

ARQUIVO_MEMORIA = "produtos_postados.txt"

if not os.path.exists(ARQUIVO_MEMORIA):
    open(ARQUIVO_MEMORIA, "w").close()


def carregar_memoria():

    with open(ARQUIVO_MEMORIA,"r") as f:
        return set(l.strip() for l in f.readlines())


def salvar_produto(pid):

    with open(ARQUIVO_MEMORIA,"a") as f:
        f.write(pid+"\n")


produtos_vistos = carregar_memoria()


def numero(txt):
    return int(re.sub("[^0-9]", "", txt))


def extrair_id(link):

    match = re.search(r'MLB\d+', link)

    if match:
        return match.group()

    return link


def limpar_titulo(t):
    t = re.sub(r'\s+', ' ', t)
    return t.strip()


def enviar_telegram(msg, imagem):

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    data = {
        "chat_id": CHAT_ID,
        "caption": msg,
        "photo": imagem
    }

    requests.post(url, data=data)


def detectar_frete(card):

    txt = card.text.lower()

    if "frete grátis" in txt or "full" in txt:
        return True

    return False


def detectar_vendas(card):

    txt = card.text.lower()

    if "vendid" in txt or "+100" in txt or "+500" in txt:
        return True

    return False


def produto_viral(card):

    score = 0

    if detectar_vendas(card):
        score += 1

    if detectar_frete(card):
        score += 1

    return score >= 1


def buscar():

    for termo in buscas:

        print("\n🔎 Buscando:", termo)

        url = f"https://lista.mercadolivre.com.br/{termo.replace(' ','-')}"

        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.text, "html.parser")

        cards = soup.select(".poly-card")

        for card in cards[:30]:

            try:

                titulo = card.select_one(".poly-component__title").text
                titulo = limpar_titulo(titulo)

                link = card.select_one("a.poly-component__title")["href"]

                if "click1" in link:
                    continue

                produto_id = extrair_id(link)

                if produto_id in produtos_vistos:
                    continue

                preco_atual = card.select_one(".andes-money-amount__fraction")
                preco_antigo = card.select_one(".andes-money-amount--previous .andes-money-amount__fraction")

                if not preco_antigo:
                    continue

                preco_atual = numero(preco_atual.text)
                preco_antigo = numero(preco_antigo.text)

                desconto = int((preco_antigo - preco_atual) / preco_antigo * 100)

                if desconto < 30:
                    continue

                if not produto_viral(card):
                    continue

                imagem = card.select_one("img")["src"]

                frete_msg = ""
                if detectar_frete(card):
                    frete_msg = "🚚 Frete bom\n"

                msg = f"""
🔥 ACHADINHO RELÂMPAGO

🛍 {titulo}

💰 De: R${preco_antigo}
💸 Por: R${preco_atual}

🔥 {desconto}% OFF
{frete_msg}

🛒 {link}

⚡ Promoção pode acabar a qualquer momento
"""

                print(msg)

                enviar_telegram(msg, imagem)

                produtos_vistos.add(produto_id)
                salvar_produto(produto_id)

                return

            except:
                continue


while True:

    buscar()

    print("\n⏳ Próximo achadinho em 20 minutos...\n")

    time.sleep(1200)
