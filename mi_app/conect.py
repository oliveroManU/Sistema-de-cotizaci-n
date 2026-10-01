from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

DB_PATH = os.path.join(basedir, 'Velazcres.db')


@app.route('/')
def home():
    conn = sqlite3.connect('Velazcres.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.execute('SELECT * FROM PRODUCTO')
    productos = cursor.fetchall()   # ← obtienes los datos
    conn.close()
    return render_template('index.html', productos=productos)    

@app.route('/mostrador')
def mostrador():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor = conn.execute('SELECT * FROM PRODUCTO')
    productos = cursor.fetchall()
    conn.close()
    return render_template('mostrador.html', productos=productos)    

@app.route('/producto/<int:producto_id>')
def editar_producto(producto_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor = conn.execute('SELECT * FROM PRODUCTO WHERE CODIGO = ?', (producto_id,))
        producto = cursor.fetchone()
    
    if producto is None:
        return "Producto no encontrado", 404
    return render_template('editar.html', producto=producto)


@app.route('/producto/<int:producto_id>', methods=['POST'])
def actualizar_producto(producto_id):
    nombre = request.form.get('NOMBRE')
    precio = request.form.get('PRECIO')
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE PRODUCTO SET NOMBRE = ?, PRECIO = ? WHERE CODIGO = ? ',
            (nombre, precio, producto_id)
        )
        
    conn.commit()
    
    
    
    return redirect(url_for('mostrador'))

@app.route('/cotizacion-int', methods=['POST'])
def cotizacion_int():
    nombre = request.form['nombre']
    precio = float(request.form['precia'])
    cantidad = int(request.form['cantidad'])
    tasapago = request.form['tasapago']
    moneda =  request.form['moneda']
    precioventa = request.form['precioventa']
    ganancia = request.form['ganacia']
    conn = sqlite3.connect('Velazcres.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuario (NOMBRE, PRECIO, CANTIDAD, TASAPAGO, MONEDA, PRECIOVENTA, GANANCIA) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                   (nombre, precio, cantidad, tasapago, moneda, precioventa, ganancia   ))
    conn.close()