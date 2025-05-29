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

    cursor.execute("SELECT 1 FROM usuarios WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return "email_exists"
    
    cursor.execute("SELECT 1 FROM usuarios WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return "username_exists"

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
        return "integrity_error"
    except Exception as e:
        print(f"Error desconocido al registrar usuario: {e}")
        conn.close()
        return False

def find_user_by_username(username):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # (id, nombre, password_hash, username, email, telefono) - ORDEN IMPORTANTE
    cursor.execute("SELECT id, nombre, password_hash, username, email, telefono FROM usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, apellido1, username, email, telefono FROM usuarios")
    users = cursor.fetchall()
    conn.close()
    return users

# --- ¡NUEVAS FUNCIONES PARA EL PERFIL! ---

def get_user_by_id(user_id):
    """
    Recupera todos los datos de un usuario por su ID.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Asegúrate de seleccionar TODAS las columnas que quieres mostrar/editar en el perfil
    cursor.execute("SELECT id, nombre, apellido1, apellido2, username, email, telefono, password_hash FROM usuarios WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user(user_id, nombre, apellido1, apellido2, username, email, telefono):
    """
    Actualiza la información de un usuario.
    No actualiza la contraseña desde aquí.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        # Primero, verifica si el nuevo email o username ya existen para OTRO usuario
        cursor.execute("SELECT id FROM usuarios WHERE email = ? AND id != ?", (email, user_id))
        if cursor.fetchone():
            conn.close()
            return False # Email ya existe para otro usuario

        cursor.execute("SELECT id FROM usuarios WHERE username = ? AND id != ?", (username, user_id))
        if cursor.fetchone():
            conn.close()
            return False # Username ya existe para otro usuario

        cursor.execute(
            "UPDATE usuarios SET nombre = ?, apellido1 = ?, apellido2 = ?, username = ?, email = ?, telefono = ? WHERE id = ?",
            (nombre, apellido1, apellido2, username, email, telefono, user_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al actualizar usuario {user_id}: {e}")
        conn.close()
        return False

def delete_user(user_id):
    """
    Elimina un usuario de la base de datos por su ID.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al eliminar usuario {user_id}: {e}")
        conn.close()
        return False