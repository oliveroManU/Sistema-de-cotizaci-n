import sqlite3
conexion = sqlite3.connect('Velazcres.db')
cursorBD = conexion.cursor()

def tableexist(nombreTabla):
    cursorBD.execute('''SELECT COUNT(NAME) FROM SQLITE_MASTER WHERE TYPE = 'table' AND name = '{}' '''.format(nombreTabla))
    if cursorBD.fetchone()[0] == 1:
        return True
    else:
        cursorBD.execute('''CREATE TABLE PRODUCTO (CODIGO INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT, PRECIO REAL, TASAPAGO REAL, GANANCIA REAL, PRECIOVENTA REAL)''')
    return False

tableexist('PRODUCTO')

def insert(nombre, precio, tasapago, ganancia, precioventa):
    cursorBD.execute('''INSERT INTO PRODUCTO (NOMBRE, PRECIO, TASAPAGO, GANANCIA, PRECIOVENTA) VALUES (?,?,?,?,?)''', (nombre, precio, tasapago, ganancia, precioventa))
    conexion.commit()

def select():
    cursorBD.execute('''SELECT * FROM PRODUCTO''')
    X1=[]
    for filaEncontrada in cursorBD.fetchall():
        X1.append(filaEncontrada)
    return X1 


def update(codigo, diccionario):
    VV = ['NOMBRE', 'PRECIO', 'TASAPAGO', 'GANACIA', 'PRECIOVENTA']
    for key in diccionario.keys():
        if key not in VV:
            raise Exception('Esa columna no existe')
        else:
            cursorBD.execute(f"'''UPDATE PRODUCTO SET {key} = ? WHERE CODIGO = ? '''(valor, codigo)")
    conexion.commit()

def delete(codigo):
    cursorBD.execute('''DELETE FROM PRODUCTO WHERE CODIGO = {} '''.format(codigo))
    conexion.commit()
    