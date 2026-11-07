import os
import sqlite3
import requests
import json
from functools import wraps
import pdfkit
import urllib3
from bs4 import BeautifulSoup
from PIL import Image
from flask import render_template, request, redirect, url_for, flash, make_response, current_app
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from . import app, login_manager

def SaveglobalHistory(conn, user_action, action, opdetails):
    currentdate = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
    details = json.dumps(opdetails, ensure_ascii=False, sort_keys=True)
    conn.execute(
        'INSERT INTO GLOBAL_HISTORY (USER_ACTION, ACTION, DATE_HOUR, OPERATION_DETAILS) '
        'VALUES (?, ?, ?, ?)',
        (user_action, action, currentdate, details)
    )

urllib3.disable_warnings()
UPLOAD_FOLDER = os.path.join(app.root_path, '..', 'static', 'img', 'productos')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def connect_db():
    return sqlite3.connect(
        os.path.join(current_app.instance_path, "Velazcress.db")
    )


# MODELO USUARIO + LOADER

class Usuario(UserMixin):
    def __init__(self, id, nombre, email, nivel, activo=True):
        self.id = int(id)
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


@login_manager.user_loader
def load_user(user_id):
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        'SELECT id, nombre, email, nivel, activo FROM usuarios WHERE id = ?',
        (int(user_id),)
    ).fetchone()
    conn.close()
    if row:
        return Usuario(row['id'], row['nombre'], row['email'], row['nivel'], row['activo'])
    return None


# DECORADOR ADMIN
# No se como funciona, pero es importante

def admin_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash('Solo administradores pueden acceder aquí.', 'no')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return wrapper

# ─────────────────────────────────────────────
# OBTENER TASA BCV
# ─────────────────────────────────────────────
def obtener_tasa_bcv(moneda="euro"):
    url = 'https://www.bcv.org.ve'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers, verify=False, timeout=10)
        r.encoding = "utf-8"
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            node = soup.find('div', id=moneda)
            if node:
                strong = node.find('strong', class_='strong-tb')
                if strong:
                    return float(strong.get_text(strip=True).replace(",", "."))
    except Exception as e:
        print(f"Error al obtener tasa BCV ({moneda}): {e}")
    return None

# HOME

@app.route('/')
@login_required
def home():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    productos = conn.execute('SELECT * FROM productos').fetchall()
    clientes  = conn.execute('SELECT * FROM clientes').fetchall()
    tasa_bcv_dolar = obtener_tasa_bcv("dolar")
    
    conn.close()
    return render_template('index.html', productos=productos, clientes=clientes, tasa_bcv_dolar=tasa_bcv_dolar)



# ─────────────────────────────────────────────
# LOGIN / LOGOUT
# ─────────────────────────────────────────────

# Inicio de sesión

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        conn = connect_db()
        conn.row_factory = sqlite3.Row
        row = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        conn.close()

        if not row or not check_password_hash(row['password_hash'], password):
            flash('Correo o contraseña incorrectos.', 'no')
            return redirect(url_for('login'))

        if not row['activo']:
            flash('Tu cuenta está desactivada. Contacta al administrador.', 'no')
            return redirect(url_for('login'))

        user = Usuario(row['id'], row['nombre'], row['email'], row['nivel'], row['activo'])
        login_user(user)
        flash(f'Bienvenido, {user.nombre} ({user.nivel}).', 'si')

        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/') or next_page.startswith('//'):
            next_page = url_for('home')
        return redirect(next_page)

    return render_template('login.html')

# cierre de sesión

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.', 'si')
    return redirect(url_for('login'))

# ─────────────────────────────────────────────
# ADMIN: Apartado de administración de usuarios
# ─────────────────────────────────────────────


@app.route('/admin/usuarios')
@admin_required
def admin_usuarios():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    usuarios = conn.execute(
        'SELECT id, nombre, email, nivel, activo FROM usuarios ORDER BY id DESC'
    ).fetchall()
    conn.close()
    return render_template('admin_usuarios.html', usuarios=usuarios)

# Introducir a nuevo usuario

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

    conn = connect_db()
    try:
        cursor = conn.execute(
            'INSERT INTO usuarios (nombre, email, password_hash, nivel, activo) VALUES (?, ?, ?, ?, 1)',
            (nombre, email, generate_password_hash(password), nivel)
        )
        SaveglobalHistory(
            conn, f'{current_user.nombre} (ID: {current_user.id})',
            'Crear usuario',
            {'usuario_id': cursor.lastrowid, 'nombre': nombre, 'email': email, 'nivel': nivel}
        )
        conn.commit()
        flash(f'Usuario {nombre} creado como {nivel}.', 'si')
    except sqlite3.IntegrityError:
        conn.rollback()
        flash('Ese correo ya existe.', 'no')
    except sqlite3.Error:
        conn.rollback()
        current_app.logger.exception('Error al crear usuario y registrar el historial.')
        flash('No se pudo crear el usuario.', 'no')
    finally:
        conn.close()

    return redirect(url_for('admin_usuarios'))

# Seguridad: No permitir que un administrador se desactive o elimine a sí mismo

@app.route('/admin/usuarios/<int:user_id>/toggle', methods=['POST'])
@admin_required
def admin_toggle_usuario(user_id):
    if int(user_id) == current_user.id:
        flash('No puedes desactivar tu propia cuenta.', 'no')
        return redirect(url_for('admin_usuarios'))

    conn = connect_db()
    try:
        conn.row_factory = sqlite3.Row
        usuario = conn.execute(
            'SELECT id, nombre, email, nivel, activo FROM usuarios WHERE id = ?', (user_id,)
        ).fetchone()
        if usuario is None:
            flash('Usuario no encontrado.', 'no')
            return redirect(url_for('admin_usuarios'))

        nuevo_estado = 1 - usuario['activo']
        conn.execute('UPDATE usuarios SET activo = ? WHERE id = ?', (nuevo_estado, user_id))
        SaveglobalHistory(
            conn, f'{current_user.nombre} (ID: {current_user.id})',
            'Activar usuario' if nuevo_estado else 'Desactivar usuario',
            {'usuario_id': user_id, 'nombre': usuario['nombre'], 'email': usuario['email']}
        )
        conn.commit()
        flash('Estado del usuario actualizado.', 'si')
    except sqlite3.Error:
        conn.rollback()
        current_app.logger.exception('Error al cambiar el estado del usuario y registrar el historial.')
        flash('No se pudo actualizar el estado del usuario.', 'no')
    finally:
        conn.close()
    
    return redirect(url_for('admin_usuarios'))

# Restablecer contraseña de un usuario

@app.route('/admin/usuarios/<int:user_id>/reset', methods=['POST'])
@admin_required
def admin_reset_password(user_id):
    nueva = request.form.get('nueva_password', '')
    if len(nueva) < 6:
        flash('La contraseña debe tener al menos 6 caracteres.', 'no')
        return redirect(url_for('admin_usuarios'))

    conn = connect_db()
    try:
        conn.row_factory = sqlite3.Row
        usuario = conn.execute(
            'SELECT id, nombre, email FROM usuarios WHERE id = ?', (user_id,)
        ).fetchone()
        if usuario is None:
            flash('Usuario no encontrado.', 'no')
            return redirect(url_for('admin_usuarios'))

        conn.execute(
            'UPDATE usuarios SET password_hash = ? WHERE id = ?',
            (generate_password_hash(nueva), user_id)
        )
        SaveglobalHistory(
            conn, f'{current_user.nombre} (ID: {current_user.id})',
            'Restablecer contraseña de usuario',
            {'usuario_id': user_id, 'nombre': usuario['nombre'], 'email': usuario['email']}
        )
        conn.commit()
        flash('Contraseña actualizada.', 'si')
    except sqlite3.Error:
        conn.rollback()
        current_app.logger.exception('Error al restablecer contraseña y registrar el historial.')
        flash('No se pudo actualizar la contraseña.', 'no')
    finally:
        conn.close()
    return redirect(url_for('admin_usuarios'))

# Eliminar usuario

@app.route('/admin/usuarios/<int:user_id>/eliminar', methods=['POST'])
@admin_required
def admin_eliminar_usuario(user_id):
    if int(user_id) == current_user.id:
        flash('No puedes eliminar tu propia cuenta.', 'no')
        return redirect(url_for('admin_usuarios'))

    conn = connect_db()
    try:
        conn.row_factory = sqlite3.Row
        usuario = conn.execute(
            'SELECT id, nombre, email, nivel FROM usuarios WHERE id = ?', (user_id,)
        ).fetchone()
        if usuario is None:
            flash('Usuario no encontrado.', 'no')
            return redirect(url_for('admin_usuarios'))

        conn.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
        SaveglobalHistory(
            conn, f'{current_user.nombre} (ID: {current_user.id})',
            'Eliminar usuario',
            {'usuario_id': user_id, 'nombre': usuario['nombre'],
             'email': usuario['email'], 'nivel': usuario['nivel']}
        )
        conn.commit()
        flash('Usuario eliminado.', 'si')
    except sqlite3.Error:
        conn.rollback()
        current_app.logger.exception('Error al eliminar usuario y registrar el historial.')
        flash('No se pudo eliminar el usuario.', 'no')
    finally:
        conn.close()
    return redirect(url_for('admin_usuarios'))


# ─────────────────────────────────────────────
# MOSTRADOR
# ─────────────────────────────────────────────

@app.route('/mostrador')
@login_required
def mostrador():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('mostrador.html', productos=productos)

# ─────────────────────────────────────────────
# PRODUCTO: INTRODUCIR / EDITAR / ACTUALIZAR / IMAGEN
# ─────────────────────────────────────────────
@app.route('/producto/<int:producto_id>')
@login_required
def editar_producto(producto_id):
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (producto_id,)).fetchone()
    conn.close()

    if producto is None:
        return "Producto no encontrado", 404
    return render_template('editar.html', producto=producto)


@app.route('/producto/<int:producto_id>', methods=['POST'])
@login_required
def actualizar_producto(producto_id):
    nombre   = request.form.get('nombre')
    marca    = request.form.get('marca')
    precio   = request.form.get('precio')
    cantidad = request.form.get('cantidad')

    conn = connect_db()
    conn.execute(
        'UPDATE productos SET nombre = ?, precio = ?, marca = ?, cantidad = ? WHERE id = ?',
        (nombre, precio, marca, cantidad, producto_id)
    )
    conn.commit()
    conn.close()

    flash('Producto actualizado.', 'si')
    return redirect(url_for('mostrador'))


@app.route('/producto/<int:producto_id>/imagen', methods=['POST'])
@login_required
def subir_imagen(producto_id):
    archivo = request.files.get('imagen')

    if not archivo or archivo.filename == '':
        flash('No seleccionaste ninguna imagen.', 'no')
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
        img.save(os.path.join(UPLOAD_FOLDER, nombre_final), 'JPEG', quality=90)
        flash('Imagen actualizada.', 'si')
    except Exception as e:
        flash(f'Error al procesar la imagen: {e}', 'no')

    return redirect(url_for('editar_producto', producto_id=producto_id))

# ─────────────────────────────────────────────
# COTIZACIÓN
# ─────────────────────────────────────────────
@app.route('/cotizacion_int', methods=['GET', 'POST'])
@login_required
def cotizacion_int():
    tasa_bcv_dolar = obtener_tasa_bcv("dolar")
    tasa_bcv_euro  = obtener_tasa_bcv("euro")

    conn = connect_db()
    conn.row_factory = sqlite3.Row

    if request.method == 'POST':
        try:
            nombre       = request.form.get('nombre')
            marca        = request.form.get('marca')
            precio       = float(request.form.get('precio-producto', 0) or 0)
            cantidad     = int(request.form.get('cantidad-producto', 0) or 0)
            preciounidad = float(request.form.get('precioporunidad', 0) or 0)
            tasapago     = float(request.form.get('tasapago', 0) or 0)
            moneda       = request.form.get('moneda')
            preciod      = float(request.form.get('preciod', 0) or 0)
            precioventa  = float(request.form.get('precio-venta', 0) or 0)
            gananciaD    = float(request.form.get('gananciaD', 0) or 0)
            gananciaBs   = float(request.form.get('gananciaBs', 0) or 0)

            cursor = conn.execute(
                'INSERT INTO productos (nombre, marca, precio, cantidad, precioporunidad, '
                'moneda, tasapago, precioD, precio_venta, ganancia_estimadaD, ganancia_estimadaBs) '
                'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (nombre, marca, precio, cantidad, preciounidad, moneda, tasapago,
                 preciod, precioventa, gananciaD, gananciaBs)
            )
            SaveglobalHistory(
                conn, f'{current_user.nombre} (ID: {current_user.id})',
                'Crear producto',
                {'producto_id': cursor.lastrowid, 'nombre': nombre, 'precio': precio,
                 'cantidad': cantidad, 'precio_venta': precioventa}
            )
            conn.commit()
            flash('Producto registrado.', 'si')
        except (ValueError, TypeError) as e:
            conn.rollback()
            flash(f'Error en los datos: {e}', 'no')
        except sqlite3.Error:
            conn.rollback()
            current_app.logger.exception('Error al crear producto.')
            flash('No se pudo registrar el producto.', 'no')

    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()
    return render_template('insersion.html',
                           tasa_bcv_dolar=tasa_bcv_dolar,
                           tasa_bcv_euro=tasa_bcv_euro,
                           productos=productos)

# ─────────────────────────────────────────────
# REGISTROS COTIZACIONES
# ─────────────────────────────────────────────
@app.route('/registros_cotizaciones')
@login_required
def registros_cotizaciones():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    registroscot = conn.execute('SELECT * FROM reg_cotizaciones ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('registros_cotizaciones.html', registroscot=registroscot)


@app.route('/productos/<int:productos_id>')
@login_required
def editar_productos1(productos_id):
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    productos = conn.execute('SELECT * FROM productos WHERE id = ?', (productos_id,)).fetchone()
    conn.close()

    tasa_bcv_dolar = obtener_tasa_bcv("dolar")
    tasa_bcv_euro  = obtener_tasa_bcv("euro")

    if productos is None:
        return "Producto no encontrado", 404
    return render_template('editarlistado.html',
                           productos=productos,
                           tasa_bcv_euro=tasa_bcv_euro,
                           tasa_bcv_dolar=tasa_bcv_dolar)


@app.route('/productos/<int:productos_id>', methods=['POST'])
@login_required
def actualizar_productos1(productos_id):
    try:
        nombre_producto    = request.form.get('nombre_producto')
        marca_producto     = request.form.get('marca_producto')
        precio             = float(request.form.get('precio-producto', 0) or 0)
        cantidad           = int(request.form.get('cantidad-producto', 0) or 0)
        preciounidad       = float(request.form.get('precioporunidad', 0) or 0)
        tasapago           = float(request.form.get('tasapago', 0) or 0)
        preciod            = float(request.form.get('preciod', 0) or 0)
        precioventa        = float(request.form.get('precio-venta', 0) or 0)
        gananciaD          = float(request.form.get('ValorActualD', 0) or 0)
        gananciaBs         = float(request.form.get('gananciaBs', 0) or 0)
        gananciasobrecosto = float(request.form.get('gananciasobrecosto', 0) or 0)
        margen_ganancia    = float(request.form.get('margen-ganancia', 0) or 0)
        monto_iva          = float(request.form.get('monto-iva', 0) or 0)
        precio_con_iva     = float(request.form.get('precio-con-iva', 0) or 0)
        monto_iva_d        = float(request.form.get('monto-iva-d', 0) or 0)
        tasa_hoy           = float(request.form.get('tasapagohoy', 0) or 0)
        porcentaje         = float(request.form.get('porcentajecompraventa', 0) or 0)

        conn = connect_db()
        try:
            conn.row_factory = sqlite3.Row
            anterior = conn.execute(
                'SELECT precio, cantidad, precioporunidad, tasapago, precioD, precio_venta, '
                'ganancia_estimadaD, ganancia_estimadaBs FROM productos WHERE id = ?',
                (productos_id,)
            ).fetchone()
            if anterior is None:
                flash('Producto no encontrado.', 'no')
                return redirect(url_for('registros_cotizaciones'))

            conn.execute(
                'UPDATE productos SET precio = ?, cantidad = ?, precioporunidad = ?, tasapago = ?, '
                'precioD = ?, precio_venta = ?, ganancia_estimadaD = ?, ganancia_estimadaBs = ? '
                'WHERE id = ?',
                (precio, cantidad, preciounidad, tasapago, preciod, precioventa,
                 gananciaD, gananciaBs, productos_id)
            )

            conn.execute('''
                INSERT INTO reg_cotizaciones (
                    producto_id, nombre_producto, marca_producto, precio_unitario, cantidad,
                    precio_total, tasa_bcv, porcentaje_ganancia, precio_venta, ganancia_bs,
                    ganancia_usd, ganancia_sobre_costo, margen_ganancia, monto_iva,
                    precio_con_iva, monto_iva_usd
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                productos_id, nombre_producto, marca_producto, preciounidad, cantidad,
                precio, tasa_hoy, porcentaje, precioventa, gananciaBs, gananciaD,
                gananciasobrecosto, margen_ganancia, monto_iva, precio_con_iva, monto_iva_d
            ))
            cotizacion_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

            SaveglobalHistory(
                conn, f'{current_user.nombre} (ID: {current_user.id})',
                'Editar producto',
                {
                    'producto_id': productos_id,
                    'antes': dict(anterior),
                    'despues': {
                        'precio': precio, 'cantidad': cantidad,
                        'precioporunidad': preciounidad, 'tasapago': tasapago,
                        'precioD': preciod, 'precio_venta': precioventa,
                        'ganancia_estimadaD': gananciaD, 'ganancia_estimadaBs': gananciaBs
                    }
                }
            )
            SaveglobalHistory(
                conn, f'{current_user.nombre} (ID: {current_user.id})',
                'Registrar cotización',
                {
                    'cotizacion_id': cotizacion_id,
                    'producto_id': productos_id,
                    'nombre': nombre_producto,
                    'precio': precio,
                    'cantidad': cantidad,
                    'precio_venta': precioventa
                }
            )
            conn.commit()
        except sqlite3.Error:
            conn.rollback()
            current_app.logger.exception('Error al editar producto y registrar la cotización.')
            flash('No se pudo guardar el producto y la cotización.', 'no')
            return redirect(url_for('editar_productos1', productos_id=productos_id))
        finally:
            conn.close()

        flash('Producto y cotización guardados correctamente.', 'si')
        return redirect(url_for('mostrador'))

    except (ValueError, TypeError) as e:
        flash(f'Error en los datos: {e}', 'no')
        return redirect(url_for('editar_productos1', productos_id=productos_id))


@app.route('/eliminar/<int:productos_id>', methods=["POST"])
@login_required
def eliminar_producto1(productos_id):
    conn = connect_db()
    try:
        conn.row_factory = sqlite3.Row
        producto = conn.execute('SELECT * FROM productos WHERE id = ?', (productos_id,)).fetchone()
        if producto is None:
            flash('Producto no encontrado.', 'no')
            return redirect(url_for('registros_cotizaciones'))

        conn.execute("DELETE FROM productos WHERE id = ?", (productos_id,))
        SaveglobalHistory(
            conn, f'{current_user.nombre} (ID: {current_user.id})',
            'Eliminar producto',
            {'producto_id': productos_id, 'datos': dict(producto)}
        )
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        current_app.logger.exception('Error al eliminar producto y registrar el historial.')
        flash('No se pudo eliminar el producto.', 'no')
        return redirect(url_for('registros_cotizaciones'))
    finally:
        conn.close()

    flash('Producto eliminado.', 'si')
    return redirect(url_for('registros_cotizaciones'))

# ─────────────────────────────────────────────
# Registrar CLIENTES
# ─────────────────────────────────────────────
@app.route('/cliente/guardar', methods=['POST'])
@login_required
def guardar_cliente():
    nombre    = request.form.get('nombre-cliente', '').strip()
    rif = request.form.get('RIF', '').strip()
    direccion = request.form.get('direccion-cliente', '').strip()
    email = request.form.get('email', '').strip()
    telefono = request.form.get('telefono', '').strip()

    if not nombre:
        flash('El nombre del cliente es obligatorio.', 'no')
        return redirect(url_for('home'))

    conn = connect_db()
    try:
        cursor = conn.execute(
            'INSERT INTO clientes (nombre, RIF, direccion, email, telefono) VALUES (?, ?, ?, ?, ?)',
            (nombre, rif, direccion, email, telefono )
        )
        SaveglobalHistory(
            conn, f'{current_user.nombre} (ID: {current_user.id})',
            'Crear cliente',
            {'cliente_id': cursor.lastrowid, 'nombre': nombre}
        )
        conn.commit()
        flash('Cliente guardado exitosamente.', 'si')
    except sqlite3.Error:
        conn.rollback()
        current_app.logger.exception('Error al registrar cliente y guardar el historial.')
        flash('No se pudo registrar el cliente.', 'no')
    finally:
        conn.close()

    return redirect(url_for('home'))

@app.route('/guardar_cotizacion_clientes', methods=['POST'])
def guardar_cotizacion_clientes():
    cliente = request.form.get('nombre-cliente-c', 'Cliente Sin Nombre')
    productos     = request.form.getlist('producto[]')
    precios_unid  = request.form.getlist('precioporunidad[]')
    cantidades    = request.form.getlist('cantidad-producto[]')
    precios       = request.form.getlist('precio-producto[]')
    tasas         = request.form.getlist('tasapagohoy[]')
    porcentajes   = request.form.getlist('porcentajecompraventa[]')
    precios_venta = request.form.getlist('precio-venta[]')
    valores_d     = request.form.getlist('ValorActualD[]')
    ganancias     = request.form.getlist('gananciasobrecosto[]')
    margenes      = request.form.getlist('margen-ganancia[]')
    descuentos    = request.form.getlist('descuento[]')
    pdescuentos   = request.form.getlist('pdescuento[]')
    descuentos_bs = request.form.getlist('descuentobs[]')
    descuentos_d  = request.form.getlist('descuentod[]')

    # ---- NUEVOS CAMPOS DEL TOTAL ----
    subtotal      = request.form.get('total-general', '')
    monto_iva     = request.form.get('monto-iva-bn', '')
    tasa_hoy      = request.form.get('tasapagob', '')

    def to_float(s):
        try:
            return float(s.replace(',', '.')) if s and s.strip() else 0.0
        except ValueError:
            return 0.0

    subtotal_f  = to_float(subtotal)
    monto_iva_f = to_float(monto_iva)
    tasa_f      = to_float(tasa_hoy)

    conn = connect_db()
    cur  = conn.cursor()

    def limpiar_numero(lista, index, es_entero=False):
        try:
            if index >= len(lista) or not lista[index].strip():
                return 0 if es_entero else 0.0
            valor = lista[index].replace(',', '.')
            return int(float(valor)) if es_entero else float(valor)
        except (ValueError, TypeError):
            return 0 if es_entero else 0.0

    try:
        # INSERT del pedido con los totales
        cur.execute("""
            INSERT INTO pedidos (fecha, cliente, tasa, subtotal, total_iva)
            VALUES (datetime('now'), ?, ?, ?, ?)
        """, (cliente, tasa_f, subtotal_f, monto_iva_f))
        pedido_id = cur.lastrowid

        print(f"DEBUG: Recibí {len(productos)} productos. Datos: {productos}")

        for i in range(len(productos)):
            if not productos[i] or productos[i].strip() == '':
                continue

            p_unitario = limpiar_numero(precios_unid, i)
            cant       = limpiar_numero(cantidades, i, es_entero=True)
            p_total    = limpiar_numero(precios, i)
            tasa       = limpiar_numero(tasas, i)
            porcentaje = limpiar_numero(porcentajes, i)
            p_venta    = limpiar_numero(precios_venta, i)
            v_dolar    = limpiar_numero(valores_d, i)
            ganancia   = limpiar_numero(ganancias, i)
            margen     = limpiar_numero(margenes, i)
            desc       = limpiar_numero(descuentos, i)
            p_desc     = limpiar_numero(pdescuentos, i)
            desc_bs    = limpiar_numero(descuentos_bs, i)
            desc_d     = limpiar_numero(descuentos_d, i)

            cur.execute("""
                INSERT INTO detalle_pedido
                  (pedido_id, codigo_producto, cliente_nombre, precio_unitario, cantidad,
                   precio, tasa_pago, porcentaje_cv, precio_venta,
                   valor_d, ganancia_sobre_costo, margen_ganancia,
                   descuento, pdescuento, descuento_bs, descuento_d)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pedido_id, productos[i], cliente,
                p_unitario, cant, p_total, tasa,
                porcentaje, p_venta, v_dolar, ganancia,
                margen, desc, p_desc, desc_bs, desc_d
            ))

        conn.commit()
        print("✅ ¡Cotización guardada con éxito!")

    except Exception as e:
        conn.rollback()
        print(f"❌ ERROR CRÍTICO: {e}")
        return f"Error al guardar los detalles: {e}", 500
    finally:
        conn.close()

    return redirect(url_for('home'))

@app.route('/historial_cotizaciones')
def historial_cotizaciones():
    conn = connect_db()
    cur = conn.cursor()
    
    # 1. Traemos todos los pedidos (cabecera)
    cur.execute("""
        SELECT id, fecha, cliente, tasa, subtotal, subtotal_d, 
               porc_descuento, subtotal_descuento, total_iva, subtotal_descuento_d 
        FROM pedidos 
        ORDER BY fecha DESC
    """)
    pedidos_db = cur.fetchall()
    
    pedidos = []
    
    # 2. Por cada pedido, buscamos sus productos y calculamos su total
    for p in pedidos_db:
        pedido_id = p[0]
        
        cur.execute("""
            SELECT codigo_producto, cantidad, precio_unitario, precio, tasa_pago, porcentaje_cv, 
            precio_venta, valor_d, ganancia_sobre_costo, descuento, descuento_bs, descuento_d 
            FROM detalle_pedido 
            WHERE pedido_id = ?
        """, (pedido_id,))
        productos = cur.fetchall()
        
        pedidos.append({
            'id': p[0],
            'fecha': p[1],
            'cliente': p[2],
            'tasa': p[3],
            'subtotal': p[4],
            'subtotal_d': p[5],
            'porc_descuento': p[6],
            'subtotal_descuento': p[7],
            'total_iva': p[8],
            'subtotal_descuento_d': p[9],
            'productos': productos
        })
    conn.close()
    
    return render_template('historial.html', pedidos=pedidos)
# Función para imprimir pdfs

@app.route('/descargar_pdf/<int:id>')
@login_required
def descargar_pdf(id):
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    rc = conn.execute('SELECT * FROM reg_cotizaciones WHERE id = ?', (id,)).fetchone()
    conn.close()

    if not rc:
        flash('Cotización no encontrada.', 'no')
        return redirect(url_for('registros_cotizaciones'))

    html = render_template('pdf_cotizacion.html', rc=rc)

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }

    pdf = pdfkit.from_string(html, False, options=options)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=cotizacion_{id}.pdf'
    return response

@app.route('/descargar_pdf2/<int:id>')
@login_required
def descargar_pdf2(id):
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 1. Buscar la cabecera del pedido
    pedido = cur.execute('SELECT * FROM pedidos WHERE id = ?', (id,)).fetchone()
    
    if not pedido:
        conn.close()
        flash('Cotización no encontrada.', 'error')
        return redirect(url_for('historial_cotizaciones'))

    # 2. Buscar los productos de ese pedido
    productos = cur.execute('SELECT * FROM detalle_pedido WHERE pedido_id = ?', (id,)).fetchall()
    
    conn.close()

    # 3. Renderizar la plantilla pasando el pedido y sus productos
    html = render_template('pdf_cotizacion2.html', pedido=pedido, productos=productos)

    # 4. Opciones del PDF (puedes dejarlas igual)
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None # <-- IMPORTANTE: Añade esto si usas imágenes o CSS locales
    }

    try:
        # Generar el PDF en memoria
        pdf = pdfkit.from_string(html, False, options=options)
    except Exception as e:
        # Si wkhtmltopdf no está instalado o falla, lanzará un error
        flash(f'Error al generar PDF: {e}', 'error')
        return redirect(url_for('historial_cotizaciones'))

    # 5. Devolver el PDF (inline lo abre en el navegador, attachment lo descarga)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=pedido_{id}.pdf'
    return response