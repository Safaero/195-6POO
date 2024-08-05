from flask import Flask, request, render_template, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdflask'

app.secret_key = 'mysecretkey'

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/home')
def home():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_medicos')
        consultaA = cursor.fetchall()
        return render_template('index.html', albums=consultaA)
    except Exception as e:
        print(f"Error al realizar la consulta en la tabla tb_medicos: {e}")
        return render_template('index.html', albums=[])


@app.route('/registros')
def registros():
    return render_template('registros.html')


@app.route('/consulta')
def consulta():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tb_medicos')
    medicos = cursor.fetchall()
    return render_template('consulta.html', medicos=medicos)


@app.route('/expedientes')
def expedientes():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_pacientes')
        pacientes = cursor.fetchall()
        return render_template('expedientes.html', pacientes=pacientes)
    except Exception as e:
        print(f"Error al realizar la consulta en la tabla tb_pacientes: {e}")
        return render_template('expedientes.html', pacientes=[])


@app.route('/guardarPaciente', methods=['POST'])
def guardarPaciente():
    if request.method == 'POST':
        fnombre = request.form['txtnombre']
        fpaciente = request.form['txtpaciente']
        ffecha = request.form['txtfecha']
        fsintomas = request.form['txtsintomas']
        fdiagnostico = request.form['txtdiagnostico']
        ftratamiento = request.form['txttratamiento']
        festudios = request.form['txtestudios']

        cursor = mysql.connection.cursor()

        # Verificar si el médico existe en la tabla tb_medicos
        cursor.execute(
            'SELECT * FROM tb_medicos WHERE nombre = %s', (fnombre,))
        medico = cursor.fetchone()

        if medico is None:
            flash('El nombre del médico no existe en la tabla de médicos.')
            return redirect(url_for('expedientes'))

        # Insertar el nuevo paciente
        cursor.execute(
            'INSERT INTO tb_pacientes (nombre, paciente, fecha, sintomas, diagnostico, tratamiento, estudios) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (fnombre, fpaciente, ffecha, fsintomas, fdiagnostico, ftratamiento, festudios))
        mysql.connection.commit()
        flash('Expediente generado correctamente')
        return redirect(url_for('expedientes'))


@app.route('/guardarMedico', methods=['POST'])
def guardarMedico():
    if request.method == 'POST':
        fnombre = request.form['txtnombre']
        fcorreo = request.form['txtcorreo']
        frol = request.form['txtrol']
        fcedula = request.form['txtcedula']
        frfc = request.form['txtrfc']
        fcontraseña = request.form['txtcontraseña']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO tb_medicos (nombre, correo, id_roles, cedula, rfc, contraseña) VALUES (%s, %s, %s, %s, %s, %s)',
                       (fnombre, fcorreo, frol, fcedula, frfc, fcontraseña))
        mysql.connection.commit()
        flash('Medico integrado correctamente')
        return redirect(url_for('consulta'))


@app.route('/editarPaciente/<int:id>', methods=['GET', 'POST'])
def editarPaciente(id):
    if request.method == 'POST':
        fnombre = request.form['txtnombre']
        fpaciente = request.form['txtpaciente']
        ffecha = request.form['txtfecha']
        fsintomas = request.form['txtsintomas']
        fdiagnostico = request.form['txtdiagnostico']
        ftratamiento = request.form['txttratamiento']
        festudios = request.form['txtestudios']

        cursor = mysql.connection.cursor()
        cursor.execute(
            'UPDATE tb_pacientes SET nombre=%s, paciente=%s, fecha=%s, sintomas=%s, diagnostico=%s, tratamiento=%s, estudios=%s WHERE id=%s',
            (fnombre, fpaciente, ffecha, fsintomas, fdiagnostico, ftratamiento, festudios, id))
        mysql.connection.commit()
        flash('Paciente actualizado correctamente')
        return redirect(url_for('expedientes'))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_pacientes WHERE id=%s', (id,))
        paciente = cursor.fetchone()
        return render_template('editar_paciente.html', paciente=paciente)


@app.route('/eliminarPaciente/<int:id>', methods=['GET', 'POST'])
def eliminarPaciente(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM tb_pacientes WHERE id=%s', (id,))
    mysql.connection.commit()
    flash('Paciente eliminado correctamente')
    return redirect(url_for('expedientes'))


@app.route('/editarMedico/<int:id>', methods=['POST'])
def editarMedico(id):
    if request.method == 'POST':
        fnombre = request.form['txtnombre']
        fcorreo = request.form['txtcorreo']
        frol = request.form['txtrol']
        fcedula = request.form['txtcedula']
        frfc = request.form['txtrfc']
        fcontraseña = request.form['txtcontraseña']

        cursor = mysql.connection.cursor()
        cursor.execute(
            'UPDATE tb_medicos SET nombre=%s, correo=%s, id_roles=%s, cedula=%s, rfc=%s, contraseña=%s WHERE id=%s',
            (fnombre, fcorreo, frol, fcedula, frfc, fcontraseña, id))
        mysql.connection.commit()
        flash('Médico actualizado exitosamente.')
        return redirect(url_for('consulta'))


@app.route('/eliminarMedico/<int:id>', methods=['GET', 'POST'])
def eliminarMedico(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM tb_medicos WHERE id=%s', (id,))
    mysql.connection.commit()
    flash('Médico eliminado correctamente')
    return redirect(url_for('consulta'))


@app.errorhandler(404)
def paginando(e):
    return 'Sintaxis incorrecta'


if __name__ == '__main__':
    app.run(debug=True, port=7000)
