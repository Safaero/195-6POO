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
    return render_template('index.html')

@app.route('/registros')
def registros():
    return render_template('registros.html')

@app.route('/consulta')
def consulta():
        cursor= mysql.connection.cursor();
        cursor.execute('select * from tb_medicos')
        medicos= cursor.fetchall()

        return render_template ('consulta.html',medicos=medicos)	
    
@app.route('/expedientes')
def expedientes():
    return render_template('expedientes.html')

@app.route('/guardarPaciente',methods=['POST'])
def guardarPaciente():
    if request.method == 'POST':
        fnombre= request.form ['txtnombre']
        fpaciente= request.form ['txtpaciente']
        ffecha= request.form ['txtfecha']
        #print(titulo,artista,anio)
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO tb_pacientes (nombre,paciente,fecha) VALUES (%s,%s,%s)',(fnombre,fpaciente,ffecha))
        mysql.connection.commit()
        flash ('Expediente generado correctamente')
        return redirect(url_for('expedientes'))

@app.route('/guardarMedico',methods=['POST'])
def guardarMedico():
    if request.method == 'POST':
        fnombre= request.form ['txtnombre']
        fcorreo= request.form ['txtcorreo']
        frol= request.form ['txtrol']
        fcedula = request.form ['txtcedula']
        frfc = request.form ['txtrfc']
        fcontraseña = request.form ['txtcontraseña']
        #print(titulo,artista,anio)
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO tb_medicos (nombre,correo,id_roles,cedula,rfc,contraseña) VALUES (%s,%s,%s,%s,%s,%s)',(fnombre,fcorreo,frol,fcedula,frfc,fcontraseña))
        mysql.connection.commit()
        flash ('medico integrado correctamente')
        return redirect(url_for('consulta'))
     
@app.errorhandler(404)     
def paginando(e):
    return 'sintaxis incorrecta'
     
if __name__ == '__main__':
    app.run(debug=True, port=7000)