import os
import sqlite3
from werkzeug.security import generate_password_hash

# Forzar que use la misma ruta que conect.py
basedir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(basedir, 'Velazcress.db')

print(f"Conectando a la base de datos en: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)


# 2. Generar el hash real para 'admin123'
hash_real = generate_password_hash('admin123')

# 3. Insertar el admin o actualizarlo si ya existe
conn.execute('''
    INSERT INTO usuarios (nombre, email, password_hash, nivel, activo) 
    VALUES ('Administrador', 'admin@velazcress.com', ?, 'admin', 1)
    ON CONFLICT(email) DO UPDATE SET 
        password_hash = excluded.password_hash,
        nivel = excluded.nivel,
        activo = 1
''', (hash_real,))

conn.commit()
conn.close()

print("¡Éxito! Usuario admin creado/actualizado.")
print(f"Correo: admin@velazcress.com")
print(f"Contraseña: admin123")