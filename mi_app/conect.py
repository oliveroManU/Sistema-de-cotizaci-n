from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    conn = sqlite3.connect('Velazcres.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.execute('SELECT * FROM PRODUCTO')
    productos = cursor.fetchall()   # ← obtienes los datos
    conn.close()
    return render_template('index.html', productos=productos)    
