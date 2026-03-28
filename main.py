import threading
from bot import bot
from app import app

def run_bot():
    print("🤖 Bot activo")
    bot.infinity_polling(none_stop=True)

def run_web():
    print("🌐 Web activa")
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_web()