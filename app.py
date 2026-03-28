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
# 🔐 CONTROL
# ==============================

bot_activo = True
usuarios_autorizados = {int(MI_ID)}  # solo tú por defecto

def autorizado(user_id):
    return user_id in usuarios_autorizados

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
        "/on - Activar bot\n"
        "/off - Desactivar bot\n"
        "/adduser ID - Agregar usuario\n"
        "/deluser ID - Eliminar usuario\n"
        "/users - Ver autorizados\n"
        "/location - Solicitar ubicación\n"
    )

@bot.message_handler(commands=['id'])
def get_id(msg):
    bot.reply_to(msg, f"🆔 Tu ID es: {msg.chat.id}")

@bot.message_handler(commands=['info'])
def info(msg):
    estado = "Activo ✅" if bot_activo else "Apagado ❌"
    bot.reply_to(msg,
        f"🧠 BROQUICALIFAXX CORE\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📡 Estado: {estado}\n"
        f"⚙️ Sistema: Flask + Telegram Bot\n"
        f"👑 Creador: BROQUI\n"
        f"🔥 Versión: 2.0"
    )

# ==============================
# 🔘 CONTROL ON / OFF
# ==============================

@bot.message_handler(commands=['on'])
def encender(msg):
    global bot_activo
    if not autorizado(msg.chat.id):
        return
    bot_activo = True
    bot.reply_to(msg, "🟢 Bot ACTIVADO")

@bot.message_handler(commands=['off'])
def apagar(msg):
    global bot_activo
    if not autorizado(msg.chat.id):
        return
    bot_activo = False
    bot.reply_to(msg, "🔴 Bot DESACTIVADO")

# ==============================
# 👥 USUARIOS
# ==============================

@bot.message_handler(commands=['adduser'])
def add_user(msg):
    if not autorizado(msg.chat.id):
        return
    try:
        user_id = int(msg.text.split()[1])
        usuarios_autorizados.add(user_id)
        bot.reply_to(msg, f"✅ Usuario {user_id} agregado")
    except:
        bot.reply_to(msg, "❌ Uso: /adduser ID")

@bot.message_handler(commands=['deluser'])
def del_user(msg):
    if not autorizado(msg.chat.id):
        return
    try:
        user_id = int(msg.text.split()[1])
        usuarios_autorizados.discard(user_id)
        bot.reply_to(msg, f"🗑 Usuario {user_id} eliminado")
    except:
        bot.reply_to(msg, "❌ Uso: /deluser ID")

@bot.message_handler(commands=['users'])
def ver_users(msg):
    if not autorizado(msg.chat.id):
        return
    lista = "\n".join([str(u) for u in usuarios_autorizados])
    bot.reply_to(msg, f"👥 Usuarios autorizados:\n{lista}")

# ==============================
# 📍 UBICACIÓN (CONSENTIDA)
# ==============================

@bot.message_handler(commands=['location'])
def pedir_ubicacion(msg):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn = telebot.types.KeyboardButton("📍 Compartir ubicación", request_location=True)
    markup.add(btn)

    bot.send_message(msg.chat.id,
        "📍 Presiona el botón para compartir tu ubicación",
        reply_markup=markup
    )

@bot.message_handler(content_types=['location'])
def recibir_ubicacion(msg):
    lat = msg.location.latitude
    lon = msg.location.longitude

    bot.send_message(msg.chat.id,
        f"📍 Ubicación recibida:\nLat: {lat}\nLon: {lon}\n"
        f"https://maps.google.com/?q={lat},{lon}"
    )

# ==============================
# 🌐 RUTAS WEB
# ==============================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    global bot_activo

    if not bot_activo:
        return jsonify({"status": "off"}), 403

    try:
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        foto = request.files['foto']

        fecha_hora = datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")

        reporte = (
            f"┏━━━━━━━━━━━━━━━━━━━━━━┑\n"
            f"║   ┣► 📸 Selfie tomada\n"
            f"║   ┣► 👑 BROQUICALIFAXX\n"
            f"║   ┣► 🕒 {fecha_hora}\n"
            f"║   ┣► 👤 {nombre}\n"
            f"║   ┣► 📱 {telefono}\n"
            f"║   ┣► 🌐 {request.remote_addr}\n"
            f"║   ┣► 🧾 {request.headers.get('User-Agent')}\n"
            f"┗━━━━━━━━━━━━━━━━━━━━━┙"
        )

        bot.send_photo(MI_ID, foto, caption=reporte)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==============================
# 🤖 INICIO
# ==============================

def iniciar_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=iniciar_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))