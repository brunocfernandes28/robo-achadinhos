import requests
import time
import sqlite3
import random

TOKEN = "7943259231:AAGrv6bYjdGABhKrr9W2i_roYWDmCcYKIhk"
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

# -------------------------
# BANCO DE DADOS
# -------------------------

conn = sqlite3.connect("historico.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos(
id TEXT PRIMARY KEY
)
""")

conn.commit()

# -------------------------
# TELEGRAM
# -------------------------

def enviar_telegram(msg, imagem):

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    data = {
        "chat_id": CHAT_ID,
        "caption": msg,
        "photo": imagem
    }

    requests.post(url, data=data)

# -------------------------
# HISTÓRICO
# -------------------------

def produto_existe(pid):

    cursor.execute("SELECT id FROM produtos WHERE id=?", (pid,))
    return cursor.fetchone() is not None

def salvar_produto(pid):

    cursor.execute("INSERT INTO produtos VALUES(?)", (pid,))
    conn.commit()

# -------------------------
# DETECTORES
# -------------------------

def calcular_desconto(preco, preco_antigo):

    if preco_antigo == None:
        return 0

    desconto = int((preco_antigo - preco) / preco_antigo * 100)

    return desconto

def produto_viral(vendidos):

    return vendidos >= 100

def erro_preco(preco, preco_antigo):

    if preco_antigo == None:
        return False

    desconto = calcular_desconto(preco, preco_antigo)

    return desconto >= 70

def cupom_oficial(item):

    try:

        if item["installments"]["rate"] == 0:
            return True
    except:
        pass

    return False

# -------------------------
# PROCESSAR PRODUTO
# -------------------------

def processar_produto(p):

    try:

        pid = p["id"]

        if produto_existe(pid):
            return False

        titulo = p["title"]

        preco = p["price"]

        preco_antigo = p.get("original_price")

        link = p["permalink"]

        imagem = p["thumbnail"]

        vendidos = p["sold_quantity"]

        desconto = calcular_desconto(preco, preco_antigo)

        viral = produto_viral(vendidos)

        erro = erro_preco(preco, preco_antigo)

        cupom = cupom_oficial(p)

        if desconto < 30 and not viral and not erro and not cupom:
            return False

        alerta = ""

        if desconto >= 50:
            alerta += "🚨 SUPER OFERTA\n"

        if erro:
            alerta += "⚠️ POSSÍVEL ERRO DE PREÇO\n"

        if viral:
            alerta += "🔥 PRODUTO VIRAL\n"

        if cupom:
            alerta += "🎟 PROMOÇÃO / CUPOM\n"

        msg=f"""
{alerta}

🛍 {titulo}

💰 De: R${preco_antigo}
💸 Por: R${preco}

🔥 {desconto}% OFF
📦 {vendidos} vendidos

🛒 {link}

⚡ Promoção pode acabar a qualquer momento
"""

        print(msg)

        enviar_telegram(msg, imagem)

        salvar_produto(pid)

        return True

    except:
        return False

# -------------------------
# BUSCA NORMAL
# -------------------------

def busca_normal():

    termo=random.choice(buscas)

    print("\n🔎 Busca normal:", termo)

    url=f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&limit=50"

    r=requests.get(url)

    data=r.json()

    produtos=data["results"]

    for p in produtos:

        if processar_produto(p):

            return True

    return False

# -------------------------
# RADAR PROMOÇÕES NOVAS
# -------------------------

def radar_promocoes():

    termo=random.choice(buscas)

    print("\n🚨 Radar promoção:", termo)

    url=f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&sort=date_desc&limit=50"

    r=requests.get(url)

    data=r.json()

    produtos=data["results"]

    for p in produtos:

        if processar_produto(p):

            return True

    return False

# -------------------------
# LOOP PRINCIPAL
# -------------------------

contador=0

while True:

    try:

        if contador % 3 == 0:

            radar_promocoes()

        else:

            busca_normal()

        contador+=1

        print("\n⏳ Próximo scan em 3 minutos...\n")

        time.sleep(180)

    except:

        time.sleep(60)
