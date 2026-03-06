import requests
import time
import sqlite3
import random
from datetime import datetime

TOKEN = "7943259231:AAGrv6bYjdGABhKrr9W2i_roYWDmCcYKIhk"
CHAT_ID = "-1003895577987"

POSTS_POR_HORA = 3

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

# --------------------
# BANCO
# --------------------

conn = sqlite3.connect("historico.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos(
id TEXT PRIMARY KEY
)
""")

conn.commit()

# --------------------
# CONTROLE POSTS
# --------------------

posts_hora = 0
hora_atual = datetime.now().hour

# --------------------
# TELEGRAM
# --------------------

def enviar(msg, imagem):

    global posts_hora

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    data = {
        "chat_id": CHAT_ID,
        "caption": msg,
        "photo": imagem
    }

    requests.post(url, data=data)

    posts_hora += 1

# --------------------
# HISTORICO
# --------------------

def existe(pid):

    cursor.execute("SELECT id FROM produtos WHERE id=?", (pid,))
    return cursor.fetchone() is not None


def salvar(pid):

    cursor.execute("INSERT INTO produtos VALUES(?)", (pid,))
    conn.commit()

# --------------------
# DESCONTO
# --------------------

def desconto(preco, antigo):

    if not antigo:
        return 0

    return int((antigo-preco)/antigo*100)

# --------------------
# PROCESSAR
# --------------------

def processar(p):

    global posts_hora
    global hora_atual

    try:

        if datetime.now().hour != hora_atual:

            posts_hora = 0
            hora_atual = datetime.now().hour

        if posts_hora >= POSTS_POR_HORA:

            print("🚫 limite de posts")
            return False

        pid = p["id"]

        if existe(pid):
            return False

        titulo = p["title"]
        preco = p["price"]
        antigo = p.get("original_price")
        vendidos = p["sold_quantity"]
        link = p["permalink"]

        img = p["thumbnail"].replace("-I.jpg","-O.jpg")

        desc = desconto(preco, antigo)

        aprovado = False
        alerta = ""

        print("\nProduto analisado")
        print(titulo)
        print("Desconto:", desc)
        print("Vendidos:", vendidos)

        if desc >= 25:

            alerta="🔥 OFERTA"
            aprovado=True

        if vendidos >= 50:

            alerta="🔥 PRODUTO VIRAL"
            aprovado=True

        if antigo and desc >= 70:

            alerta="⚠️ ERRO DE PREÇO"
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

# --------------------
# RADARES
# --------------------

def radar_normal():

    termo=random.choice(buscas)

    print("🔎 busca:",termo)

    url=f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&limit=200"

    r=requests.get(url)

    data=r.json()

    for p in data["results"]:

        if processar(p):
            break


def radar_viral():

    termo=random.choice(buscas)

    print("🔥 viral:",termo)

    url=f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&sort=sold_quantity_desc&limit=200"

    r=requests.get(url)

    data=r.json()

    for p in data["results"]:

        if processar(p):
            break


def radar_promocao():

    termo=random.choice(buscas)

    print("🚨 promoção:",termo)

    url=f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&sort=date_desc&limit=200"

    r=requests.get(url)

    data=r.json()

    for p in data["results"]:

        if processar(p):
            break


def radar_recente():

    termo=random.choice(buscas)

    print("⚡ recente:",termo)

    url=f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&sort=last_updated_desc&limit=200"

    r=requests.get(url)

    data=r.json()

    for p in data["results"]:

        if processar(p):
            break

# --------------------
# LOOP
# --------------------

radares=["promo","viral","recente","normal"]

contador=0

while True:

    if radares[contador%4]=="promo":

        radar_promocao()

    elif radares[contador%4]=="viral":

        radar_viral()

    elif radares[contador%4]=="recente":

        radar_recente()

    else:

        radar_normal()

    contador+=1

    print("\n⏳ próximo scan 3 minutos\n")

    time.sleep(180)
