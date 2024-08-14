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
def guardar_paciente():
    # Obtener datos del formulario
    medico = request.form['medico']
    nombre = request.form['nombre']
    fecha_nac = request.form['fecha_nac']
    enfermedades = request.form.get('enfermedades', '')
    alergias = request.form.get('alergias', '')
    antecedentes_medicos = request.form.get('antecedentes_medicos', '')
    sintomas = request.form.get('sintomas', '')
    diagnostico = request.form.get('diagnostico', '')
    tratamiento = request.form.get('tratamiento', '')
    estudios = request.form.get('estudios', '')
    peso = request.form['peso']
    altura = request.form['altura']
    temperatura = request.form['temperatura']
    latidosXminuto = request.form['latidosXminuto']
    SOX = request.form['SOX']
    glucosa = request.form['glucosa']
    edad = request.form['edad']

    # Consulta SQL para insertar datos
    query = """
        INSERT INTO tb_pacientes (medico, nombre, fecha_nac, enfermedades, alergias, antecedentes_medicos, sintomas, diagnostico, tratamiento, estudios, peso, altura, temperatura, latidosXminuto, SOX, glucosa, edad) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (
        medico, nombre, fecha_nac, enfermedades, alergias, antecedentes_medicos,
        sintomas, diagnostico, tratamiento, estudios, peso, altura, temperatura,
        latidosXminuto, SOX, glucosa, edad
    )

    try:
        cursor.execute(query, data)
        db.commit()
        flash('Paciente guardado exitosamente.')
    except MySQLdb.Error as e:
        print(f"Error al guardar paciente: {e}")
        db.rollback()
        flash('Hubo un error al guardar el paciente. Intenta nuevamente.')

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
        flash('Médico integrado correctamente')
        return redirect(url_for('consulta'))


@app.route('/editarPaciente/<int:id>', methods=['GET', 'POST'])
def editarPaciente(id):
    if request.method == 'POST':
        # Recibir los datos del formulario
        fnombre = request.form['txtnombre']
        fpaciente = request.form['txtpaciente']
        ffecha = request.form['txtfecha']
        fpeso = request.form['peso']
        faltura = request.form['altura']
        ftemperatura = request.form['temperatura']
        flatidosxminuto = request.form['latidosXminuto']
        fSOX = request.form['SOX']
        fglucosa = request.form['glucosa']
        fedad = request.form['edad']
        fsintomas = request.form['txtsintomas']
        fdiagnostico = request.form['txtdiagnostico']
        ftratamiento = request.form['txttratamiento']
        festudios = request.form['txtestudios']

        # Ejecutar la actualización en la base de datos
        cursor = mysql.connection.cursor()
        cursor.execute(
            '''UPDATE tb_pacientes 
            SET medico=%s, nombre=%s, fecha_nac=%s, peso=%s, altura=%s, temperatura=%s, latidosXminuto=%s, SOX=%s, glucosa=%s, edad=%s, sintomas=%s, diagnostico=%s, tratamiento=%s, estudios=%s 
            WHERE id=%s''',
            (fnombre, fpaciente, ffecha, fpeso, faltura, ftemperatura, flatidosxminuto,
             fSOX, fglucosa, fedad, fsintomas, fdiagnostico, ftratamiento, festudios, id)
        )
        mysql.connection.commit()

        # Mensaje de confirmación
        flash('Paciente actualizado correctamente')

        # Redirigir a la vista de expedientes
        return redirect(url_for('expedientes.html'))
    else:
        # Seleccionar el paciente actual para mostrar en el formulario
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


@app.route('/editarMedico/<int:id>', methods=['GET', 'POST'])
def editarMedico(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        nombre = request.form['txtnombre']
        rfc = request.form['txtrfc']
        cedulaP = request.form['txtcedula']
        correoE = request.form['txtcorreo']
        contraseña = request.form['txtcontraseña']
        rol = request.form['txtrol']

        cursor.execute("""
            UPDATE tb_medicos
            SET nombre = %s, rfc = %s, cedula = %s, correo = %s, contraseña = %s, id_roles = %s
            WHERE id = %s
        """, (nombre, rfc, cedulaP, correoE, contraseña, rol, id))
        mysql.connection.commit()

        flash('Datos editados y almacenados correctamente')
        return redirect(url_for('consulta'))

    cursor.execute('SELECT * FROM tb_medicos WHERE id = %s', (id,))
    medico = cursor.fetchone()
    cursor.close()

    return render_template('editar_medico.html', medico=medico)


@app.route('/consultaMedicos')
def consultaMedicos():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tb_medicos')
    medicos = cursor.fetchall()
    return render_template('consulta_medicos.html', medicos=medicos)


@app.route('/eliminarMedico/<int:id>', methods=['GET', 'POST'])
def eliminarMedico(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM tb_medicos WHERE id=%s', (id,))
    mysql.connection.commit()
    flash('Médico eliminado correctamente')
    return redirect(url_for('consulta'))


@app.errorhandler(404)
def paginando(e):
    return 'Página no encontrada', 404


if __name__ == '__main__':
    app.run(debug=True, port=7000)
