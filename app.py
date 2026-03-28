from flask import Flask, request, jsonify
from bot import bot, bot_activo
from config import MI_ID
from datetime import datetime

app = Flask(__name__)

@app.route('/enviar', methods=['POST'])
def enviar():
    if not bot_activo:
        return jsonify({"status": "off"}), 403

    nombre = request.form.get('nombre')
    telefono = request.form.get('telefono')
    foto = request.files['foto']

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    bot.send_photo(
        MI_ID,
        foto,
        caption=f"{nombre} | {telefono} | {fecha}"
    )

    return jsonify({"ok": True})