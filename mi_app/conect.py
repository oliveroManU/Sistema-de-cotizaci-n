from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3
import requests
from datetime import date
from bs4 import BeautifulSoup
import urllib3

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

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
    precio = request.form.get('precio')
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE productos SET nombre = ?, precio = ? WHERE id = ? ',
            (nombre, precio, producto_id)
        )
        
    conn.commit()
    
    
    
    return redirect(url_for('mostrador'))

@app.route('/cotizacion_int', methods=['GET','POST'])
def cotizacion_int():
    tasa_bcv = obtener_tasa_bcv()
    nombre = request.form.get('nombre')
    marca = request.form.get('marca')
    precio = float(request.form.get('precio-producto', 0))
    cantidad = int(request.form.get('cantidad-producto', 0))
    preciounidad = float(request.form.get('preciounidad', 0))
    tasapago = float(request.form.get('tasapago', 0))
    moneda =  request.form.get('moneda')
    preciod = float(request.form.get('preciod', 0))
    conn = sqlite3.connect('Velazcress.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    ### anñadir : cantidad, moneda
    cursor.execute('INSERT INTO productos (nombre, marca, precio, cantidad, precioporunidad, moneda, tasapago, precioD) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                   (nombre, marca, precio, cantidad, preciounidad, moneda, tasapago, preciod  ))
    conn.commit()
    conn.close()
    return render_template('insersion.html', tasa_bcv=tasa_bcv)

###@app.route('/cotizacion_ext', methods=['GET','POST'])
""" def cotizacion_int():
    tasa_bcv = obtener_tasa_bcv()
    nombre = request.form.get('nombre')
    precio = float(request.form.get('precio', 0))
    cantidad = int(request.form.get('cantidad', 0))
    tasapago = request.form.get('tasapago')
    moneda =  request.form.get('moneda')
    precioventa = request.form.get('precioventa')
    ganancia = request.form.get('ganacia')
    conn = sqlite3.connect('Velazcres.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    ### anñadir : cantidad, moneda
    cursor.execute('INSERT INTO productos (nombre, precio, cantidad, moneda, tasapago, GANANCIA) VALUES (?, ?, ?, ?, ?)', 
                   (nombre, precio, tasapago, precioventa, ganancia   ))
    conn.commit()
    conn.close()
    return render_template('insersion.html', tasa_bcv=tasa_bcv)
"""

def obtener_tasa_bcv():
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
            tasafinder = soup.find('div', id="dolar")
            if tasafinder:
                strong = tasafinder.find('strong', class_='strong-tb')
                if strong:
                    cuptext = strong.get_text(strip=True)
                    numberbcv = float(cuptext.replace(",", "."))
                    return numberbcv
    except Exception as e:
        print(f"Error al obtener tasa BCV: {e}")
    return None


 