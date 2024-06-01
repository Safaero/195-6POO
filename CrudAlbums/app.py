from flask import Flask, request, render_template
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdflask'

mysql=MySQL(app)

@app.route('/')
def index():
    return render_template ('index.html')	

@app.route('/guardarAlbum',methods=['POST'])
def guardarAlbum():
    if request.method == 'POST':
        titulo= request.form ['txtTitulo']
        artista= request.form ['txtArtista']
        anio= request.form ['txtAnio']
        print(titulo,artista,anio)
        return 'datos recibidos en el servidor'
     
@app.errorhandler(404)     
def paginando(e):
    return 'revisa tu sintaxis: no encontrado naada'
     
if __name__ == '__main__':
    app.run(debug=True, port=3000)