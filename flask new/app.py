from flask import Flask,request

app= Flask(__name__)

#ruta basica
@app.route('/')
def principal():
    return 'Hola mundo Flask'

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