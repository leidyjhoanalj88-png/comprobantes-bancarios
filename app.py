from flask import Flask, request, jsonify, send_from_directory
import psycopg2
import psycopg2.extras
import os

app =#@4244 Flask(__name__, static_folder='static')

def get_db():
    url = os.environ['DATABASE_URL']
    if url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)
    return psycopg2.connect(url, sslmode='require')

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            nombre VARCHAR(100) NOT NULL,
            pin VARCHAR(6) NOT NULL,
            rol VARCHAR(10) DEFAULT 'user',
            estado VARCHAR(10) DEFAULT 'activo',
            comprobantes INT DEFAULT 0
        )
    ''')
    # Crear admin por defecto si no existe
    cur.execute("SELECT id FROM usuarios WHERE username='admin'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO usuarios (username, nombre, pin, rol) VALUES (%s,%s,%s,%s)",
            ('admin', 'Administrador', '123456', 'admin')
        )
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '').strip().lower()
    pin = data.get('pin', '').strip()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT * FROM usuarios WHERE LOWER(username)=%s AND pin=%s AND estado='activo'",
        (username, pin)
    )
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return jsonify({'ok': True, 'user': {
            'id': user['id'], 'username': user['username'],
            'nombre': user['nombre'], 'rol': user['rol']
        }})
    return jsonify({'ok': False, 'error': 'Usuario o PIN incorrecto'})

@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, username, nombre, rol, estado, comprobantes FROM usuarios ORDER BY id")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(list(users))

@app.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    data = request.json
    username = data.get('username', '').strip().lower()
    nombre = data.get('nombre', '').strip()
    pin = data.get('pin', '').strip()
    rol = data.get('rol', 'user')
    if not username or not nombre or not pin:
        return jsonify({'ok': False, 'error': 'Completa todos los campos'})
    if not pin.isdigit() or len(pin) != 6:
        return jsonify({'ok': False, 'error': 'El PIN debe ser 6 dígitos numéricos'})
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuarios (username, nombre, pin, rol) VALUES (%s,%s,%s,%s)",
            (username, nombre, pin, rol)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'ok': True})
    except psycopg2.errors.UniqueViolation:
        return jsonify({'ok': False, 'error': 'Ese usuario ya existe'})

@app.route('/api/usuarios/<int:uid>', methods=['PUT'])
def editar_usuario(uid):
    data = request.json
    nombre = data.get('nombre', '').strip()
    pin = data.get('pin', '').strip()
    estado = data.get('estado', 'activo')
    if not nombre:
        return jsonify({'ok': False, 'error': 'El nombre no puede estar vacío'})
    conn = get_db()
    cur = conn.cursor()
    if pin:
        if not pin.isdigit() or len(pin) != 6:
            return jsonify({'ok': False, 'error': 'El PIN debe ser 6 dígitos'})
        cur.execute("UPDATE usuarios SET nombre=%s, pin=%s, estado=%s WHERE id=%s", (nombre, pin, estado, uid))
    else:
        cur.execute("UPDATE usuarios SET nombre=%s, estado=%s WHERE id=%s", (nombre, estado, uid))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'ok': True})

@app.route('/api/usuarios/<int:uid>/toggle', methods=['POST'])
def toggle_usuario(uid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE usuarios SET estado = CASE WHEN estado='activo' THEN 'inactivo' ELSE 'activo' END WHERE id=%s", (uid,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'ok': True})

init_db()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
