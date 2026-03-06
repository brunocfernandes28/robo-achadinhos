print("ROBO ACHADINHOS V5.0 INICIADO")
import requests
import time
import sqlite3
import random
from datetime import datetime

TOKEN = "7943259231:AAGrv6bYjdGABhKrr9W2i_roYWDmCcYKIhk"
CHAT_ID = "-1003895577987"

POSTS_POR_HORA = 3

headers = {
"User-Agent":"Mozilla/5.0"
}

# categorias grandes do mercado livre
categorias = [
"MLB1430", # moda feminina
"MLB1246", # beleza
"MLB1055", # casa
"MLB1384", # bebe
"MLB1000", # eletronicos
"MLB1743"  # automotivo
]

# ----------------------
# BANCO
# ----------------------

conn = sqlite3.connect("historico.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos(
id TEXT PRIMARY KEY
)
""")

conn.commit()

# ----------------------
# CONTROLE DE POSTS
# ----------------------

posts_hora = 0
hora_atual = datetime.now().hour

# ----------------------
# TELEGRAM
# ----------------------

def enviar(msg,img):

    global posts_hora

    url=f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    data={
    "chat_id":CHAT_ID,
    "caption":msg,
    "photo":img
    }

    requests.post(url,data=data)

    posts_hora+=1

# ----------------------
# HISTORICO
# ----------------------

def existe(pid):

    cursor.execute("SELECT id FROM produtos WHERE id=?",(pid,))
    return cursor.fetchone() is not None


def salvar(pid):

    cursor.execute("INSERT INTO produtos VALUES(?)",(pid,))
    conn.commit()

# ----------------------
# DESCONTO
# ----------------------

def desconto(preco,antigo):

    if not antigo:
        return 0

    return int((antigo-preco)/antigo*100)

# ----------------------
# PROCESSAR PRODUTO
# ----------------------

def processar(p):

    global posts_hora
    global hora_atual

    try:

        if datetime.now().hour != hora_atual:

            posts_hora = 0
            hora_atual = datetime.now().hour

        if posts_hora >= POSTS_POR_HORA:

            print("🚫 limite de posts por hora")
            return False

        pid=p["id"]

        if existe(pid):
            return False

        titulo=p["title"]
        preco=p["price"]
        antigo=p.get("original_price")
        vendidos=p["sold_quantity"]
        link=p["permalink"]

        img=p["thumbnail"].replace("-I.jpg","-O.jpg")

        desc=desconto(preco,antigo)

        print("\nProduto analisado")
        print(titulo)
        print("Desconto:",desc)
        print("Vendidos:",vendidos)

        aprovado=False
        alerta=""

        if desc>=25:

            alerta="🔥 OFERTA"
            aprovado=True

        if vendidos>=50:

            alerta="🔥 PRODUTO VIRAL"
            aprovado=True

        if antigo and desc>=70:

            alerta="⚠️ POSSÍVEL ERRO DE PREÇO"
            aprovado=True

        if not aprovado:

            print("❌ reprovado")
            return False

        print("✅ aprovado")

        msg=f"""
{alerta}

🛍 {titulo}

💰 De: R${antigo}
💸 Por: R${preco}

🔥 {desc}% OFF
📦 {vendidos} vendidos

🛒 {link}

⚡ Promoção pode acabar a qualquer momento
"""

        enviar(msg,img)

        salvar(pid)

        return True

    except Exception as e:

        print("Erro:",e)
        return False

# ----------------------
# RADAR
# ----------------------

def radar():

    categoria=random.choice(categorias)

    print("\n🔎 Radar categoria:",categoria)

    url=f"https://api.mercadolibre.com/sites/MLB/search?category={categoria}&limit=50"

    r=requests.get(url,headers=headers)

    data=r.json()

    produtos=data.get("results",[])

    print("Produtos encontrados:",len(produtos))

    for p in produtos:

        if processar(p):

            break

# ----------------------
# LOOP
# ----------------------

while True:

    radar()

    print("\n⏳ próximo scan em 3 minutos\n")

    time.sleep(180)
