from flask import Flask,request,jsonify
from flask_mysqldb import MySQL

#inicializacion de la app
app= Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdflask'

mysql= MySQL(app)

#rutas
#ruta basica
@app.route('/PruebaConexion')
def PruebaConexion():
    try:
        cursor= mysql.connection.cursor()
        cursor.execute('SELECT 1')
        datos= cursor.fetchone()
        return jsonify({'status':'conexion exitosa','data':datos})
    except Exception as ex:
        return jsonify({'stattus':'error de conexion','mensaje':str(ex)})
        
#ruta basica
@app.route('/Usuario')
@app.route('/Saludar')
def saludos():
    return 'Hola Peredo ja'

#rutas con parametros

@app.route('/hi/nombre>')
def hi (nombre):
    return 'hola'+ nombre +'!!!'

#definicion demetodos detrabajo

@app.route('/formulario', methods=['GET','POST'])
def formulario():
    if request.method == 'GET':
        return 'No es seguro enviar pass por GET'
    elif request.method == 'POST':
        return 'POST si esz seguro'

@app.errorhandler(404)
def paginando(e):
    return 'revisa tu sintaxis: no encontrado naada'

if __name__ == "__main__":
    app.run(port=3000, debug=True)