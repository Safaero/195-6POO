from flask import Flask, request, render_template, url_for, redirect, flash
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdflask'

app.secret_key ='mysecretkey'

mysql=MySQL(app)

@app.route('/')
def index():
    try:
        cursor= mysql.connection.cursor();
        cursor.execute('select * from albums')
        consultaA= cursor.fetchall()
        #print(consultaA)
        return render_template ('index.html',albums=consultaA)	
    except Exception as e:
        print (e)
        
@app.route('/editar/<id>')
def editar(id):
    cur= mysql.connection.cursor()
    cur.execute('select * from albums where idAlbum=%s',[id])
    albumE= cur.fetchone()
    return render_template('editar.html',album= albumE)

@app.route('/guardarCambios/<id>',methods=['POST'])
def guardarCambios(id):
    if request.method == 'POST':
        ftitulo= request.form ['txtTitulo']
        fartista= request.form ['txtArtista']
        fanio= request.form ['txtAnio']
        #print(titulo,artista,anio)
        cursor = mysql.connection.cursor()
        cursor.execute('update albums set titulo=%s, artista=%s, anio=%s where idAlbum=%s', (ftitulo,fartista,fanio,id))
        mysql.connection.commit()
        flash ('cambios guardados correctamente')
        return redirect(url_for('index'))
    
@app.route('/guardarAlbum',methods=['POST'])
def guardarAlbum():
    if request.method == 'POST':
        ftitulo= request.form ['txtTitulo']
        fartista= request.form ['txtArtista']
        fanio= request.form ['txtAnio']
        #print(titulo,artista,anio)
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO albums (titulo,artista,anio) VALUES (%s,%s,%s)',(ftitulo,fartista,fanio))
        mysql.connection.commit()
        flash ('album guardado correctamente')
        return redirect(url_for('index'))
     
@app.errorhandler(404)     
def paginando(e):
    return 'revisa tu sintaxis: no encontrado naada'
     
if __name__ == '__main__':
    app.run(debug=True, port=3000)