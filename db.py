# db.py
import sqlite3

DATABASE_NAME = "db.db"

def connect_db():
    """Establece una conexión con la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def init_db():
    """
    Inicializa la base de datos: crea las tablas si no existen.
    Vamos a crear una tabla simple de 'usuarios' para empezar.
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    # Crear tabla 'usuarios'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"Base de datos '{DATABASE_NAME}' inicializada y tabla 'usuarios' creada/verificada.")

def insert_user(nombre, email):
    """Inserta un nuevo usuario en la base de datos."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre, email) VALUES (?, ?)", (nombre, email))
        conn.commit()
        print(f"Usuario '{nombre}' insertado correctamente.")
        return True
    except sqlite3.IntegrityError:
        print(f"Error: El email '{email}' ya existe.")
        return False
    finally:
        conn.close()

def get_all_users():
    """Obtiene todos los usuarios de la base de datos."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email FROM usuarios")
    users = cursor.fetchall()
    conn.close()
    return users

# Opcional: una función para borrar datos de prueba si es necesario
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
    # insert_user("Juan Pérez", "juan@example.com")
    # insert_user("Ana García", "ana@example.com")
    # users = get_all_users()
    # print("\nUsuarios actuales:")
    # for user in users:
    #     print(user)