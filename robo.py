print("ROBO ACHADINHOS V4.2 INICIADO")
import requests
import time
import sqlite3
import random
from datetime import datetime

TOKEN = "7943259231:AAGrv6bYjdGABhKrr9W2i_roYWDmCcYKIhk"
CHAT_ID = "-1003895577987"

POSTS_POR_HORA = 3

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

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

# --------------------
# HISTORICO
# --------------------

def existe(pid):

    cursor.execute("SELECT id FROM produtos WHERE id=?",(pid,))
    return cursor.fetchone() is not None

def salvar(pid):

    cursor.execute("INSERT INTO produtos VALUES(?)",(pid,))
    conn.commit()

# --------------------
# DESCONTO
# --------------------

def calcular_desconto(preco,antigo):

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

            posts_hora=0
            hora_atual=datetime.now().hour

        if posts_hora>=POSTS_POR_HORA:

            print("🚫 limite de posts atingido")
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

        desc=calcular_desconto(preco,antigo)

        print("\nProduto analisado")
        print("Titulo:",titulo)
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
# RADAR
# --------------------

def radar(tipo):

    termo=random.choice(buscas)

    print(f"\n🔎 Radar {tipo}: {termo}")

    if tipo=="promo":

        url=f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&sort=date_desc&limit=200"

    elif tipo=="viral":

        url=f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&sort=sold_quantity_desc&limit=200"

    elif tipo=="recente":

        url=f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&sort=last_updated_desc&limit=200"

    else:

        url=f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&limit=200"

    try:

        r=requests.get(url,headers=headers,timeout=20)

        data=r.json()

        produtos=data.get("results",[])

        print("Produtos encontrados:",len(produtos))

        # fallback
        if len(produtos)==0:

            print("⚠ API vazia → fallback busca normal")

            url=f"https://api.mercadolibre.com/sites/MLB/search?q={termo}&limit=200"

            r=requests.get(url,headers=headers)

            data=r.json()

            produtos=data.get("results",[])

            print("Produtos fallback:",len(produtos))

        for p in produtos:

            if processar(p):

                break

    except Exception as e:

        print("Erro API:",e)

# --------------------
# LOOP
# --------------------

radares=["promo","viral","recente","normal"]

contador=0

while True:

    radar(radares[contador%4])

    contador+=1

    print("\n⏳ próximo scan em 3 minutos\n")

    time.sleep(180)
