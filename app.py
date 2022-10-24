


import os
from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
import  sys
from datetime import datetime
from flask import send_from_directory


app= Flask(__name__)
app.secret_key = "develoteca"
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitio'
mysql.init_app(app)


@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/img/<imagen>')
def imagenes(imagen):
    return send_from_directory(os.path.join('templates/sitio/img'),imagen)

@app.route('/css/<archivocss>')
def css_link(archivocss):
    return send_from_directory(os.path.join('templates/sitio/css'),archivocss)


@app.route('/libros')   
def libros():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM libros")
    datos_recuperados = cursor.fetchall()
    conexion.commit()    
    return render_template('sitio/libros.html',libros = datos_recuperados)

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')


@app.route('/admin/')
def admin_index():
    
    if not 'login' in session:
        return redirect('/admin/login')
    
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('/admin/login.html')

@app.route('/admin/login', methods = ['POST'])
def admin_login_post():
    _user = request.form['txtUsuario']
    _password = request.form['txtContraseña']
    
    print(_user)
    print(_password)
    
    if _user=="admin" and _password=="123":
        session['login']= True
        session['usuario']= 'Administrador'
        return redirect('/admin')
    
    return render_template('/admin/login.html', mensaje='Acceso denegado')

@app.route('/admin/cerrar')
def admin_login_cerrar():
    session.clear()
    return redirect('/admin/login')


@app.route('/admin/libros')
def admin_libros():
    
    if not 'login' in session:
        return redirect('/admin/login')
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM libros")
    datos_recuperados = cursor.fetchall()
    conexion.commit()
    
    return render_template('admin/libros.html',libros = datos_recuperados)


@app.route('/admin/libros/guardar',methods=['POST'])
def admin_libros_guardar():
    
    if not 'login' in session:
        return redirect('/admin/login')
    
    # aqui capturamos loc campos del form
    _nombre = request.form['txtNombre']
    _archivo_imagen = request.files['txtImagen']
    _url = request.form['txtURL']
    
    tiempo= datetime.now()
    hora_actual = tiempo.strftime('%Y%H%M%S')
    if _archivo_imagen.filename != "":
        nuevoNombre = hora_actual +"_" + _archivo_imagen.filename
        
        _archivo_imagen.save('templates/sitio/img/' + nuevoNombre)
    
    #aqui se crea la conexiona a la BD y se envian los dafos con un sql
    try:
        
        sql = "INSERT INTO `libros` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL,%s,%s,%s);" 
        datos = (_nombre,nuevoNombre,_url)
        
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute(sql,datos)
        conexion.commit()
    except Exception as e:
        print(f"Ocurrio un  error ela conexion a BD conexion: {e}")
        sys.exit()
    
    return redirect('/admin/libros')
    
@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libros_borrar():
    
    if not 'login' in session:
        return redirect('/admin/login')
    
    _id = request.form['txtID']
    print(_id)
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT imagen FROM `libros` WHERE id=%s", (_id))
    id_recuperado = cursor.fetchall()
    conexion.commit()
    print(f"SELECT ID: {id_recuperado}")
    
    if os.path.exists('templates/sitio/img/'+ str(id_recuperado[0][0])):
        os.unlink('templates/sitio/img/'+ str(id_recuperado[0][0]))
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id=%s", (_id))
    conexion.commit()
    
    return redirect('/admin/libros')


if __name__ =='__main__':
    
    app.run(debug=True)