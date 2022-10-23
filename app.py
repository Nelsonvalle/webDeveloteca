

from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
import  sys

app= Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitio'
mysql.init_app(app)


@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/libros')   
def libros():
    return render_template('sitio/libros.html')


@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')


@app.route('/admin/')
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/libros')
def admin_libros():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM libros")
    datos_recuperados = cursor.fetchall()
    conexion.commit()
    print(f'SELECT: {datos_recuperados}')
    return render_template('admin/libros.html',libros = datos_recuperados)


@app.route('/admin/libros/guardar',methods=['POST'])
def admin_libros_guardar():
    # aqui capturamos loc campos del form
    _nombre = request.form['txtNombre']
    _archivo_imagen = request.files['txtImagen']
    _url = request.form['txtURL']
    
    #aqui se crea la conexiona a la BD y se envian los dafos con un sql
    try:
        
        sql = "INSERT INTO `libros` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL,%s,%s,%s);" 
        datos = (_nombre,_archivo_imagen.filename,_url)
        
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
    _id = request.form['txtID']
    print(_id)
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM libros WHERE id=%s", (_id))
    id_recuperado = cursor.fetchall()
    conexion.commit()
    print(f"SELECT ID: {id_recuperado}")
    
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id=%s", (_id))
    conexion.commit()
    
    return redirect('/admin/libros')


if __name__ =='__main__':
    
    app.run(debug=True)