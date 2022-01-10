from flask import Flask
from flask import render_template, request, redirect, url_for
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'si'
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA']= CARPETA

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/indexme')
def indexme():
    return render_template('Menu.html')


@app.route('/nosotros')
def nosotros():

    sql = "SELECT * FROM `bebidas`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    bebidas = cursor.fetchall()

    conn.commit()
    return render_template('Nosotros/index.html', bebidas=bebidas)

@app.route('/comunidades')
def comunidades():

    sql2 = "SELECT * FROM `botana`;"
    conn2 = mysql.connect()
    cursor2 = conn2.cursor()
    cursor2.execute(sql2)

    botanas = cursor2.fetchall()

    conn2.commit()

    return render_template('Comunidades/index.html', botanas=botanas)

@app.route('/eventos')
def eventos():

    sql3 = "SELECT * FROM `reservaciones`;"
    conn3 = mysql.connect()
    cursor3 = conn3.cursor()
    cursor3.execute(sql3)

    reservaciones = cursor3.fetchall()

    conn3.commit()
    return render_template('Eventos/index.html', reservaciones=reservaciones)




@app.route('/createbebidas')
def createbebidas():
    return render_template('Bebidas/create.html')

@app.route('/createbotanas')
def createbotanas():
    return render_template('botana/create.html')

@app.route('/createreservacion')
def createreservacion():
    return render_template('Reservaciones/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _descripcion = request.form['txtdescripcion']
    _tipo = request.form['listtipo']
    _cantidad = request.form['txtcantidad']
    _precio = request.form['txtprecio']
    _imagen = request.files['txtFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _imagen.filename != '':
        nuevoNombre = tiempo + _imagen.filename
        _imagen.save("uploads/"+nuevoNombre)

    sql = "insert into `bebidas` (`Id`, `Nombre`, `Descripcion`, `Tipo`, `Cantidad`, `Precio`, `Imagen`) VALUES(NULL, %s, %s, %s, %s, %s, %s);"
    datos = (_nombre, _descripcion,_tipo,_cantidad,_precio, nuevoNombre)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/indexbe')

@app.route('/store2', methods=['POST'])
def storage2():
    _nombre = request.form['txtNombre']
    _descripcion = request.form['txtdescripcion']
    _precio = request.form['txtprecio']
    _cantidad = request.form['txtcantidad']
    _imagen = request.files['txtFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _imagen.filename != '':
        nuevoNombre = tiempo + _imagen.filename
        _imagen.save("uploads/"+nuevoNombre)

    sql = "insert into `botana` (`Id`, `Nombre`, `Descripcion`, `Cantidad`, `Precio`, `Imagen`) VALUES(NULL, %s, %s, %s, %s, %s);"
    datos = (_nombre, _descripcion, _cantidad, _precio, nuevoNombre)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/indexbo')

@app.route('/store3', methods=['POST'])
def storage3():
    _nombre = request.form['txtNombre']
    _mesa = request.form['txtMesa']
    _precio = request.form['txtprecio']
    _fecha = request.form['txtFecha']
    _Hora = request.form['txtHora']

    sql = "insert into `reservaciones` (`Id`, `Nombre`, `Mesa`, `Fecha`, `Hora`, `Precio`) VALUES(NULL, %s, %s, %s, %s, %s);"
    datos = (_nombre, _mesa,_fecha, _Hora, _precio)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/indexre')

@app.route('/destroybebidas/<int:id>')
def destroybebidas(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT Imagen FROM bebidas WHERE Id=%s", (id))
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))

    cursor.execute("DELETE FROM bebidas WHERE id=%s", (id))
    conn.commit()
    return redirect('/indexbe')

@app.route('/destroybotana/<int:id>')
def destroybotana(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT Imagen FROM botana WHERE Id=%s", (id))
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))

    cursor.execute("DELETE FROM botana WHERE Id=%s", (id))
    conn.commit()
    return redirect('/indexbo')


@app.route('/destroyreservacion/<int:id>')
def destroyreservacion(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reservaciones WHERE Id=%s", (id))
    conn.commit()
    return redirect('/indexre')

@app.route('/editbebidas/<int:id>')
def editbebidas(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bebidas WHERE id=%s", (id))
    bebidas = cursor.fetchall()
    conn.commit()
    return render_template('bebidas/edit.html', bebidas=bebidas)

@app.route('/editbotana/<int:id>')
def editbotana(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM botana WHERE Id=%s", (id))
    botanas = cursor.fetchall()
    conn.commit()
    return render_template('botana/edit.html', botanas=botanas)

@app.route('/editreservaciones/<int:id>')
def editreservaciones(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reservaciones WHERE Id=%s", (id))
    reservaciones = cursor.fetchall()
    conn.commit()
    return render_template('Reservaciones/edit.html', reservaciones=reservaciones)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _descripcion = request.form['txtdescripcion']
    _tipo = request.form['listtipo']
    _cantidad = request.form['txtcantidad']
    _precio = request.form['txtprecio']

    _foto = request.files['txtFoto']
    id = request.form['txtID']

    sql = "UPDATE bebidas SET Nombre=%s, Descripcion=%s, Tipo=%s, Cantidad=%s, Precio=%s WHERE Id=%s;"

    datos = (_nombre, _descripcion, _tipo, _cantidad, _precio, id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    now = datetime.now()
    hora = now.strftime("%Y%H%M%S")

    if _foto.filename !='':
        nuevoNombre = hora + _foto.filename
        _foto.save('uploads/'+nuevoNombre)
        cursor.execute("SELECT Imagen FROM bebidas WHERE Id=%s", id)
        fila = cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE bebidas SET Imagen=%s WHERE Id=%s", (nuevoNombre, id))
        conn.commit()

    return redirect('/indexbe')

@app.route('/updatebotana', methods=['POST'])
def updatebotana():
    _nombre = request.form['txtNombre']
    _descripcion = request.form['txtdescripcion']
    _precio = request.form['txtprecio']

    _foto = request.files['txtFoto']
    id = request.form['txtID']

    sql = "UPDATE botana SET Nombre=%s, Precio=%s, Descripcion=%s WHERE Id=%s;"

    datos = (_nombre, _precio, _descripcion, id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    now = datetime.now()
    hora = now.strftime("%Y%H%M%S")

    if _foto.filename !='':
        nuevoNombre = hora + _foto.filename
        _foto.save('uploads/'+nuevoNombre)
        cursor.execute("SELECT Imagen FROM botana WHERE Id=%s", id)
        fila = cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE botana SET Imagen=%s WHERE Id=%s", (nuevoNombre, id))
        conn.commit()

    return redirect('/indexbo')


@app.route('/updatereservacion', methods=['POST'])
def updatereservacion():
    _nombre = request.form['txtNombre']
    _mesa = request.form['txtMesa']
    _Fecha = request.form['txtFecha']
    _Hora = request.form['txtHora']
    _precio = request.form['txtprecio']
    id = request.form['txtID']

    sql = "UPDATE reservaciones SET Nombre=%s, Mesa=%s, Fecha=%s, Hora=%s, Precio=%s WHERE Id=%s;"

    datos = (_nombre, _mesa, _Fecha, _Hora, _precio,id)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/indexre')


@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

if __name__ == '__main__':
    app.run(debug=True)