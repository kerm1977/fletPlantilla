# db.py
import sqlite3
import bcrypt

DATABASE_NAME = 'db.db'

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido1 TEXT NOT NULL,
            apellido2 TEXT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefono TEXT,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Base de datos 'db.db' inicializada y tabla 'usuarios' creada/verificada.")

def register_user(nombre, apellido1, apellido2, username, telefono, email, password):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Verificar si el email o username ya existen
    cursor.execute("SELECT 1 FROM usuarios WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return "email_exists"
    
    cursor.execute("SELECT 1 FROM usuarios WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return "username_exists"

    # Hashear la contraseña antes de guardarla
    # bcrypt.hashpw espera bytes, por eso .encode('utf-8')
    # .decode('utf-8') convierte el hash de bytes a string para guardarlo en la DB
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, apellido1, apellido2, username, email, telefono, password_hash) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (nombre, apellido1, apellido2, username, email, telefono, hashed_password)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error de integridad al registrar usuario: {e}")
        conn.close()
        return "integrity_error" # Esto es un fallback, ya que los checks anteriores deberían evitarlo
    except Exception as e:
        print(f"Error desconocido al registrar usuario: {e}")
        conn.close()
        return False

def find_user_by_username(username):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Asegúrate de que las columnas seleccionadas y su ORDEN coincidan con lo que esperas en LoginView
    # (id, nombre, password_hash, username, email, telefono)
    cursor.execute("SELECT id, nombre, password_hash, username, email, telefono FROM usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    """
    Recupera todos los usuarios de la base de datos.
    Útil para depuración o para mostrar una lista de usuarios.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Solo seleccionamos las columnas que necesitamos para mostrar en la lista de prueba
    cursor.execute("SELECT id, nombre, apellido1, username, email, telefono FROM usuarios")
    users = cursor.fetchall()
    conn.close()
    return users