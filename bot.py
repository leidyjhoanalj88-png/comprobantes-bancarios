import telebot
from config import TOKEN, MI_ID

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

bot_activo = True
usuarios_autorizados = {MI_ID}

def autorizado(user_id):
    return user_id in usuarios_autorizados

# =====================
# COMANDOS
# =====================

@bot.message_handler(commands=['start'])
def start(msg):
    print("START recibido")
    bot.reply_to(msg, "👑 BOT ACTIVO\nUsa /help")

@bot.message_handler(commands=['help'])
def help_cmd(msg):
    bot.reply_to(msg,
        "/start\n/help\n/info\n/id\n/on\n/off\n/adduser ID\n/users"
    )

@bot.message_handler(commands=['id'])
def get_id(msg):
    bot.reply_to(msg, f"🆔 {msg.chat.id}")

@bot.message_handler(commands=['info'])
def info(msg):
    estado = "🟢 Activo" if bot_activo else "🔴 Off"
    bot.reply_to(msg, f"Estado: {estado}")

# =====================
# CONTROL
# =====================

@bot.message_handler(commands=['on'])
def on(msg):
    global bot_activo
    if autorizado(msg.chat.id):
        bot_activo = True
        bot.reply_to(msg, "🟢 Activado")

@bot.message_handler(commands=['off'])
def off(msg):
    global bot_activo
    if autorizado(msg.chat.id):
        bot_activo = False
        bot.reply_to(msg, "🔴 Apagado")

# =====================
# USUARIOS
# =====================

@bot.message_handler(commands=['adduser'])
def adduser(msg):
    if autorizado(msg.chat.id):
        try:
            uid = int(msg.text.split()[1])
            usuarios_autorizados.add(uid)
            bot.reply_to(msg, f"✅ {uid} agregado")
        except:
            bot.reply_to(msg, "❌ Uso: /adduser ID")

@bot.message_handler(commands=['users'])
def users(msg):
    if autorizado(msg.chat.id):
        bot.reply_to(msg, "\n".join(map(str, usuarios_autorizados)))

# =====================
# DEBUG IMPORTANTE
# =====================

@bot.message_handler(func=lambda m: True)
def debug(msg):
    print("📩 MENSAJE:", msg.text)