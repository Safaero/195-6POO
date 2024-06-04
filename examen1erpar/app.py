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

@app.route('/numeroalcuadrado')
def numeroalcuadrado():
    return render_template ('numeroalcuadrado.html')

@app.route('/form')
def form():
    return render_template ('form.html')	

@app.route('/enviar',methods=['POST'])
def guardarAlbum():
    if request.method == 'POST':
        nombre= request.form ['nombre']
        edad= request.form ['edad']
        print(nombre,edad)
        return 'datos recibidos en el servidor'
     
@app.errorhandler(404)     
def paginando(e):
    return 'ruta inexistente'
     
if __name__ == '__main__':
    app.run(debug=True, port=3500)