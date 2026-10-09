from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import os
import sqlite3
import requests
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


@app.route('/')
def home():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    cursor = conn.execute('SELECT * FROM productos')
    productos = cursor.fetchall()   # ← obtienes los datos
    conn.close()
    return render_template('index.html', productos=productos)    

@app.route('/mostrador')
def mostrador():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor = conn.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return render_template('mostrador.html', productos=productos)    

@app.route('/producto/<int:producto_id>')
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
def listado():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor = conn.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return render_template('listado.html', productos=productos) 

@app.route('/productos/<int:productos_id>')
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
def eliminar_producto1(productos_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM productos WHERE id = ?", (productos_id,))    
    conn.commit()
    conn.close()
    
    flash('Producto eliminado')
    return redirect(url_for('listado'))
    
    
    
    


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


 