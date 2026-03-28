import threading
from bot import bot
from app import app

def run_bot():
    bot.infinity_polling(skip_pending=True)

# 👇 IMPORTANTE
threading.Thread(target=run_bot).start()

# 👇 esto lo usa gunicorn
application = app