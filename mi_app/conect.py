from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
import requests
from functools import wraps
from datetime import date
from bs4 import BeautifulSoup
import urllib3

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# Carpeta destino
UPLOAD_FOLDER = os.path.join('static', 'img', 'productos')
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

DB_PATH = os.path.join(basedir, 'Velazcress.db')

### login manager, para la gestion de usuario

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'          
login_manager.login_message = 'Debes iniciar sesión para acceder.'
login_manager.login_message_category = 'no'

@app.route('/')
def home():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    cursor = conn.execute('SELECT * FROM productos')
    productos = cursor.fetchall()   # ← obtienes los datos
    conn.close()
    return render_template('index.html', productos=productos)    

class usuario(UserMixin):
    def __init__(self, id, nombre, email, nivel, activo=True):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.nivel = nivel
        self.activo = bool(activo)
        
    @property
    def is_admin(self):
        return self.nivel == 'admin'
    
    @property
    def is_active(self):
        return self.activo 
        
### Loader user para la gestion de usuario
        
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        'SELECT id, nombre, email, nivel, activo FROM usuarios WHERE id = ?', (user_id,)    
    ).fetchone()
    conn.close()
    if row:
        return usuario(row['id'], row['nombre'], row['email'], row['nivel'], row['activo'])
    return None

### Sin esto no sirve el admin_required,(no se porque pero es necesario)
### es para que solo los administradores puedan acceder a ciertas rutas

def admin_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash('Solo administradores pueden acceder aquí.', 'no')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return wrapper

### Esto es para el login, es un poco MUY largo

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        row = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        conn.close()

        if not row or not check_password_hash(row['password_hash'], password):
            flash('Correo o contraseña incorrectos.', 'no')
            return redirect(url_for('login'))

        if not row['activo']:
            flash('Tu cuenta está desactivada. Contacta al administrador.', 'no')
            return redirect(url_for('login'))

        user = usuario(row['id'], row['nombre'], row['email'], row['nivel'], row['activo'])
        login_user(user)

        flash(f'Bienvenido, {user.nombre} ({user.nivel}).', 'si')
        next_page = request.args.get('next')
        # Evitar open redirect
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('home')
        return redirect(next_page)

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.', 'si')
    return redirect(url_for('login'))

### Finaliza lo refernete al login

### administración de usuarios

@app.route('/admin/usuarios')
@admin_required
def admin_usuarios():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    usuarios = conn.execute(
        'SELECT id, nombre, email, nivel, activo FROM usuarios ORDER BY id DESC'
    ).fetchall()
    conn.close()
    return render_template('admin_usuarios.html', usuarios=usuarios)


@app.route('/admin/usuarios/nuevo', methods=['POST'])
@admin_required
def admin_crear_usuario():
    nombre   = request.form.get('nombre', '').strip()
    email    = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    nivel    = request.form.get('nivel', 'operador').strip()

    if nivel not in ('admin', 'operador'):
        flash('Nivel inválido.', 'no')
        return redirect(url_for('admin_usuarios'))

    if not nombre or not email or len(password) < 6:
        flash('Datos incompletos o contraseña muy corta (mín. 6).', 'no')
        return redirect(url_for('admin_usuarios'))

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            'INSERT INTO usuarios (nombre, email, password_hash, nivel, activo) VALUES (?, ?, ?, ?, 1)',
            (nombre, email, generate_password_hash(password), nivel)
        )
        conn.commit()
        conn.close()
        flash(f'Usuario {nombre} creado como {nivel}.', 'si')
    except sqlite3.IntegrityError:
        flash('Ese correo ya existe.', 'no')

    return redirect(url_for('admin_usuarios'))


@app.route('/admin/usuarios/<int:user_id>/toggle', methods=['POST'])
@admin_required
def admin_toggle_usuario(user_id):
    if user_id == current_user.id:
        flash('No puedes desactivar tu propia cuenta.', 'no')
        return redirect(url_for('admin_usuarios'))

    conn = sqlite3.connect(DB_PATH)
    conn.execute('UPDATE usuarios SET activo = 1 - activo WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('Estado del usuario actualizado.', 'si')
    return redirect(url_for('admin_usuarios'))


@app.route('/admin/usuarios/<int:user_id>/reset', methods=['POST'])
@admin_required
def admin_reset_password(user_id):
    nueva = request.form.get('nueva_password', '')
    if len(nueva) < 6:
        flash('La contraseña debe tener al menos 6 caracteres.', 'no')
        return redirect(url_for('admin_usuarios'))

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        'UPDATE usuarios SET password_hash = ? WHERE id = ?',
        (generate_password_hash(nueva), user_id)
    )
    conn.commit()
    conn.close()
    flash('Contraseña actualizada.', 'si')
    return redirect(url_for('admin_usuarios'))


@app.route('/admin/usuarios/<int:user_id>/eliminar', methods=['POST'])
@admin_required
def admin_eliminar_usuario(user_id):
    if user_id == current_user.id:
        flash('No puedes eliminar tu propia cuenta.', 'no')
        return redirect(url_for('admin_usuarios'))

    conn = sqlite3.connect(DB_PATH)
    conn.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('Usuario eliminado.', 'si')
    return redirect(url_for('admin_usuarios'))

### Ruta del login para 
"""
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mostrador'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password =request.form.get('password', '')
    
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            'SELECT * FROM usuarios WHERE email = ?', (email,)    
        ).fetchone()
        conn.close
    
        if row and check_password_hash(row['password_hash'], password):
            user = usuario(row['id'], row['nombre'], row['email'], row['nivel'])
            login_user(user)
            flash(f'Bienvenido, {usuario.nombre}', 'si')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('mostrador'))
    
        flash('Correo o contraseña incorrectos', 'no')
    
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('mostrar'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip().lower
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')
        
        if not nombre or not email or not password:
            flash('Todos los campos son obligatorios', 'no')
            return redirect(url_for('registro'))
        
        if password != password2:
            flash('las contraseñas no coinciden', 'no')
            return redirect(url_for('registro'))    
        
        if len(password) < 6:
            flash('minimo 6 caracteres', 'no')
            return redirect(url_for('registro'))    
        
        password_hash = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute(
                'INSERT INTO usuarios (nombre, email, password_hash, nivel) VALUES (?, ?, ?, ?)',
                (nombre, email, password_hash, 'cl') 
            )
            conn.commit()
            conn.close()
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'si')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Ese correo ya está registrado', 'no')
            return redirect(url_for('registro'))

    return render_template('registro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'si')
    return redirect(url_for('login'))
"""

@app.route('/mostrador')
@login_required
def mostrador():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor = conn.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return render_template('mostrador.html', productos=productos)       

@app.route('/producto/<int:producto_id>')
@login_required
def editar_producto(producto_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor = conn.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
        producto = cursor.fetchone()
    
    if producto is None:
        return "Producto no encontrado", 404
    return render_template('editar.html', producto=producto)


@app.route('/producto/<int:producto_id>', methods=['POST'])
@login_required
def actualizar_producto(producto_id):
    nombre = request.form.get('nombre')
    marca = request.form.get('marca')
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE productos SET nombre = ?, precio = ?, marca = ?, cantidad = ? WHERE id = ? ',
            (nombre, precio, marca, cantidad, producto_id)
        )
        
    conn.commit()
    
    
    
    return redirect(url_for('mostrador'))

@app.route('/producto/<int:producto_id>/imagen', methods=['POST'])
@login_required
def subir_imagen(producto_id):
    archivo = request.files.get('imagen')

    if not archivo or archivo.filename == '':
        flash('No seleccionaste ninguna imagen')
        return redirect(url_for('editar_producto', producto_id=producto_id))

    try:

        img = Image.open(archivo)

        if img.mode in ('RGBA', 'LA', 'P'):
            fondo = Image.new('RGB', img.size, (255, 255, 255))
            fondo.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = fondo
        elif img.mode != 'RGB':
            img = img.convert('RGB')
            
        nombre_final = f'{producto_id}.jpg'
        ruta_final = os.path.join(UPLOAD_FOLDER, nombre_final)
        img.save(ruta_final, 'JPEG', quality=90)

        flash('Imagen actualizada')
    except Exception as e:
        flash(f'Error al procesar la imagen: {e}')

    return redirect(url_for('editar_producto', producto_id=producto_id))


@app.route('/cotizacion_int', methods=['GET','POST'])
@login_required
def cotizacion_int():
    tasa_bcv_dolar = obtener_tasa_bcv("dolar")
    tasa_bcv_euro = obtener_tasa_bcv("euro")
    conn = sqlite3.connect('Velazcress.db')
    conn.row_factory = sqlite3.Row          
    cursor = conn.cursor()
    if request.method == 'POST':
        
        nombre = request.form.get('nombre')
        marca = request.form.get('marca')
        precio = float(request.form.get('precio-producto', 0))
        cantidad = int(request.form.get('cantidad-producto', 0))
        preciounidad = float(request.form.get('precioporunidad', 0))
        tasapago = float(request.form.get('tasapago', 0))
        moneda =  request.form.get('moneda')
        preciod = float(request.form.get('preciod', 0))
        precioventa = float(request.form.get('precio-venta', 0))
        gananciaD = float(request.form.get('gananciaD', 0))
        gananciaBs =  float(request.form.get('gananciaBs', 0))
        
        cursor.execute('INSERT INTO productos (nombre, marca, precio, cantidad, precioporunidad, moneda, tasapago, precioD, precio_venta, ganancia_estimadaD, ganancia_estimadaBs) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                   (nombre, marca, precio, cantidad, preciounidad, moneda, tasapago, preciod, precioventa, gananciaD, gananciaBs  ))
        conn.commit()
    productos = conn.execute("SELECT * FROM productos").fetchall()  
    conn.close()  
    return render_template('insersion.html', tasa_bcv_dolar=tasa_bcv_dolar, tasa_bcv_euro=tasa_bcv_euro, productos=productos)

@app.route('/listado')
@login_required
def listado():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor = conn.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return render_template('listado.html', productos=productos) 

@app.route('/productos/<int:productos_id>')
@login_required
def editar_productos1(productos_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor = conn.execute('SELECT * FROM productos WHERE id = ?', (productos_id,))
        productos = cursor.fetchone()
    tasa_bcv_dolar = obtener_tasa_bcv("dolar")
    tasa_bcv_euro = obtener_tasa_bcv("euro")
    
    if productos is None:
        return "Producto no encontrado", 404
    return render_template('editarlistado.html', productos=productos, tasa_bcv_euro=tasa_bcv_euro, tasa_bcv_dolar=tasa_bcv_dolar)


@app.route('/productos/<int:productos_id>', methods=['POST'])
@login_required
def actualizar_productos1(productos_id):
    
    try:
        
        nombre = request.form.get('nombre', '').strip()    
        marca = request.form.get('marca', '').strip()
        moneda =  request.form.get('moneda', '').strip()
        precio = float(request.form.get('precio-producto', 0))
        cantidad = int(request.form.get('cantidad-producto', 0))
        preciounidad = float(request.form.get('precioporunidad', 0))
        tasapago = float(request.form.get('tasapago', 0))  
        preciod = float(request.form.get('preciod', 0))
        precioventa = float(request.form.get('precio-venta', 0))
        gananciaD = float(request.form.get('gananciaD', 0))
        gananciaBs =  float(request.form.get('gananciaBs', 0))
        
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE productos SET precio = ?, cantidad = ?, precioporunidad = ?, tasapago = ?, precioD = ?, precio_venta = ?, ganancia_estimadaD = ?, ganancia_estimadaBs = ? WHERE id = ? ',
                (precio, cantidad, preciounidad, tasapago, preciod, precioventa, gananciaD, gananciaBs, productos_id)
            )           
            conn.commit()
    
        flash('Producto Actualizado correctamnet', 'si')
        return redirect(url_for('listado'))   
        
        
    except (ValueError,TypeError) as e:
        flash(f'error en los datos: {e}', 'no')
        return redirect(url_for('actualizar_productos1', productos_id=productos_id, ))


@app.route('/eliminar/<int:productos_id>', methods=["POST"])
@login_required
def eliminar_producto1(productos_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM productos WHERE id = ?", (productos_id,))    
    conn.commit()
    conn.close()
    
    flash('Producto eliminado')
    return redirect(url_for('listado'))
    
### registro de clientes a la base de datos

"""

@app.route('/registroclientes', methods=['GET','POST'])
def registro_clientes():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    if request.method == 'POST':
        
        nombre = request.form.get('nombre')
        rif = request.form.get('RIF')
        direccion = request.form.get('direccion')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        
        
        conn.execute('INSERT INTO productos (nombre, rif, , cantidad,) VALUES (?, ?, ?, ?, ?)', 
                   (nombre, rif, direccion, email, telefono))
        conn.commit()
    clientes = conn.execute("SELECT * FROM productos").fetchall()  
    conn.close()  
    return render_template('registroclientes.html')
"""
    
def obtener_tasa_bcv(moneda="euro"):
    """
    Obtiene la tasa oficial del BCV.
    moneda: 'euro' o 'dolar'
    """
    url = 'https://www.bcv.org.ve'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        respuesta = requests.get(url, headers=headers, verify=False, timeout=10)
        respuesta.encoding = "utf-8"

        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            tasafinder = soup.find('div', id=moneda)  # 'euro' o 'dolar'
            if tasafinder:
                strong = tasafinder.find('strong', class_='strong-tb')
                if strong:
                    cuptext = strong.get_text(strip=True)
                    return float(cuptext.replace(",", "."))
    except Exception as e:
        print(f"Error al obtener tasa BCV ({moneda}): {e}")
    return None


 