# db.py

import sqlite3
import bcrypt # Asegúrate de haber instalado: pip install bcrypt

DATABASE_NAME = "db.db"

def connect_db():
    """Establece una conexión con la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    # conn.row_factory = sqlite3.Row # Opcional: para obtener resultados como diccionarios
    return conn

def init_db():
    """
    Inicializa la base de datos: crea la tabla 'usuarios' si no existe.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    # Crear tabla 'usuarios' con todos los campos del registro
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido1 TEXT NOT NULL,
            apellido2 TEXT, -- Segundo apellido puede ser opcional
            username TEXT UNIQUE NOT NULL,
            telefono TEXT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL -- Guardamos el HASH de la contraseña
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"Base de datos '{DATABASE_NAME}' inicializada y tabla 'usuarios' creada/verificada.")

def register_user(nombre, apellido1, apellido2, username, telefono, email, password_plain):
    """
    Inserta un nuevo usuario en la base de datos.
    Hashea la contraseña antes de guardarla.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Hashear la contraseña antes de guardarla
        # bcrypt.gensalt() genera un "salt" aleatorio para cada hash, aumentando la seguridad
        password_hash = bcrypt.hashpw(password_plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellido1, apellido2, username, telefono, email, password_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nombre, apellido1, apellido2, username, telefono, email, password_hash))
        conn.commit()
        print(f"Usuario '{username}' registrado correctamente.")
        return True
    except sqlite3.IntegrityError as e:
        # Manejar errores de unicidad (email o username ya existen)
        if "UNIQUE constraint failed: usuarios.email" in str(e):
            print(f"Error: El email '{email}' ya está registrado.")
            return "email_exists"
        elif "UNIQUE constraint failed: usuarios.username" in str(e):
            print(f"Error: El nombre de usuario '{username}' ya existe.")
            return "username_exists"
        else:
            print(f"Error desconocido al registrar usuario: {e}")
            return False
    finally:
        conn.close()

def find_user_by_username(username):
    """
    Busca un usuario por su nombre de usuario.
    Retorna una tupla (id, username, password_hash) o None si no se encuentra.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password_hash FROM usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    """Obtiene todos los usuarios de la base de datos (excluyendo el hash de contraseña)."""
    conn = connect_db()
    cursor = conn.cursor()
    # Seleccionamos las columnas que queremos mostrar
    cursor.execute("SELECT id, nombre, apellido1, username, email, telefono FROM usuarios")
    users = cursor.fetchall()
    conn.close()
    return users

# Opcional: una función para borrar todos los usuarios (útil para pruebas)
def clear_users():
    """Borra todos los usuarios de la tabla (útil para pruebas)."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios")
    conn.commit()
    conn.close()
    print("Todos los usuarios eliminados.")

# Para probar la inicialización al ejecutar db.py directamente
if __name__ == "__main__":
    init_db()
    # Puedes añadir algunas inserciones de prueba aquí si quieres
    # Recuerda: si borras db.db, los usuarios de prueba se irán.
    # clear_users() # Descomentar para borrar todos los usuarios antes de añadir nuevos
    # if not find_user_by_username("testuser"): # Solo añade si no existe
    #     register_user("Test", "User", "", "testuser", "123456789", "test@example.com", "password123")
    # if not find_user_by_username("admin"):
    #     register_user("Admin", "User", "", "admin", "999999999", "admin@example.com", "adminpass")
    
    users = get_all_users()
    print("\nUsuarios actuales en la DB:")
    if users:
        for user in users:
            # user es una tupla: (id, nombre, apellido1, username, email, telefono)
            print(f"ID: {user[0]}, Nombre: {user[1]} {user[2]}, Usuario: {user[3]}, Email: {user[4]}, Teléfono: {user[5]}")
    else:
        print("No hay usuarios registrados.")