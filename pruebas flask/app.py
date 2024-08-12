from flask import Flask, request, render_template, url_for, redirect, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash  
from datetime import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdflask'
app.secret_key = 'mysecretkey'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        rfc = request.form['rfc']
        contraseña = request.form['contraseña']
        cursor = mysql.connection.cursor()
        
        cursor.execute('SELECT nombre, id_roles, contraseña FROM tb_medicos WHERE rfc = %s', [rfc])
        medico = cursor.fetchone()
        
        if medico and check_password_hash(medico[2], contraseña):
            session['nombre_medico'] = medico[0]
            session['id_roles'] = medico[1]
            
            if medico[1] == 1:
                return redirect(url_for('admin_home'))
            else:  
                return redirect(url_for('home'))
        else:
            flash('Credenciales incorrectas. Inténtalo de nuevo.')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/home')
def home():
    if 'nombre_medico' not in session:
        return redirect(url_for('login'))
    
    nombre_medico = session.get('nombre_medico', 'Doctor')
    return render_template('index.html', nombre_medico=nombre_medico)  

@app.route('/admin_home')
def admin_home():
    if 'nombre_medico' not in session:
        return redirect(url_for('login'))
    
    return render_template('admin.html')  

@app.route('/registros')
def registros():
    return render_template('registros.html')

@app.route('/consulta')
def consulta():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tb_medicos')
    medicos = cursor.fetchall()
    return render_template('consulta.html', medicos=medicos)    

@app.route('/guardarMedico', methods=['POST'])
def guardarMedico():
    if request.method == 'POST':
        fnombre = request.form['txtnombre']
        fcorreo = request.form['txtcorreo']
        frol = request.form['txtid_roles']
        fcedula = request.form['txtcedula']
        frfc = request.form['txtrfc']
        fcontraseña = request.form['txtcontraseña']

        try:
            hashed_contraseña = generate_password_hash(fcontraseña)
            cursor = mysql.connection.cursor()
            cursor.execute('''
                INSERT INTO tb_medicos (nombre, correo, id_roles, cedula, rfc, contraseña)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (fnombre, fcorreo, frol, fcedula, frfc, hashed_contraseña))

            mysql.connection.commit()
            cursor.close()
            flash('Médico guardado correctamente', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash('Error al guardar el médico: ' + str(e), 'danger')

        return redirect(url_for('registros'))

@app.route('/editarMedico/<id>')
def editarMedico(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tb_medicos WHERE id_medico=%s', [id])
    medico = cur.fetchone()
    cur.close()
    if medico:
        return render_template('editarMedico.html', medico=medico)
    else:
        flash('Médico no encontrado', 'danger')
        return redirect(url_for('consulta'))

@app.route('/ActualizarMedico/<id>', methods=['POST'])
def ActualizarMedico(id):
    if request.method == 'POST':
        try:
            fnombre = request.form['txtnombre']
            fcorreo = request.form['txtcorreo']
            frol = request.form['txtid_roles']
            fcedula = request.form['txtcedula']
            frfc = request.form['txtrfc']
            fcontraseña = request.form['txtcontraseña']
            hashed_contraseña = generate_password_hash(fcontraseña)

            cursor = mysql.connection.cursor()
            cursor.execute('''
                           UPDATE tb_medicos 
                           SET nombre=%s, correo=%s, id_roles=%s, cedula=%s, rfc=%s, contraseña=%s 
                           WHERE id_medico=%s
                           ''', (fnombre, fcorreo, frol, fcedula, frfc, hashed_contraseña, id))

            mysql.connection.commit()
            cursor.close()
            flash('Médico editado correctamente', 'info')
        except Exception as e:
            mysql.connection.rollback()
            flash('Error al actualizar el médico: ' + str(e), 'danger')

        return redirect(url_for('consulta'))

@app.route('/eliminar_medico/<int:id>', methods=['POST'])
def eliminar_medico(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM tb_medicos WHERE id_medico=%s', [id])
        mysql.connection.commit()
        cur.close()
        flash('Médico eliminado correctamente', 'success')
    except Exception as e:
        flash('Error al eliminar el médico: ' + str(e), 'danger')
    
    return redirect(url_for('consulta'))

@app.route('/registro_pacientes')
def registro_pacientes():
    return render_template('registro_pacientes.html')

@app.route('/guardarPaciente', methods=['POST'])
def guardarPaciente():
    if request.method == 'POST':
        nombre_med = request.form['txtnombre_med']
        paciente = request.form['txtpaciente']
        fecha_nac = request.form['txtfecha']
        enfermedades_cronicas = request.form.get('txtenfermedades_cronicas', '')
        alergias = request.form.get('txtalergias', '')
        antecedentes_familiares = request.form.get('txtantecedentes_familiares', '')

        try:
            cursor = mysql.connection.cursor()
            cursor.execute('''
                INSERT INTO tb_pacientes 
                (nombre_med, paciente, fecha_nac, enfermedades_cronicas, alergias, antecedentes_familiares)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (nombre_med, paciente, fecha_nac, enfermedades_cronicas, alergias, antecedentes_familiares))

            mysql.connection.commit()
            flash('Paciente registrado correctamente', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al registrar el paciente: {str(e)}', 'danger')
        
        return redirect(url_for('expedientes'))
    
@app.route('/editarPaciente/<int:id>', methods=['GET', 'POST'])
def editarPaciente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tb_pacientes WHERE id_Paciente=%s', [id])
    paciente = cur.fetchone()
    cur.close()
    if paciente:
        return render_template('editar_paciente.html', paciente=paciente)
    else:
        flash('Paciente no encontrado', 'danger')
        return redirect(url_for('expedientes'))

@app.route('/ActualizarPaciente/<int:id>', methods=['POST'])
def ActualizarPaciente(id):
    if request.method == 'POST':
        try:
            fnombre_med = request.form['txtnombre_med']
            fpaciente = request.form['txtpaciente']
            ffecha_nac = request.form['txtfecha_nac']
            fenfermedades_cronicas = request.form.get('txtenfermedades_cronicas', '')
            falergias = request.form.get('txtalergias', '')
            fantescedentes_familiares = request.form.get('txtantecedentes_familiares', '')

            cursor = mysql.connection.cursor()
            cursor.execute('''
                UPDATE tb_pacientes 
                SET nombre_med=%s, paciente=%s, fecha_nac=%s, enfermedades_cronicas=%s, alergias=%s, antecedentes_familiares=%s
                WHERE id_Paciente=%s
            ''', (fnombre_med, fpaciente, ffecha_nac, fenfermedades_cronicas, falergias, fantescedentes_familiares, id))

            mysql.connection.commit()
            cursor.close()
            flash('Paciente actualizado correctamente', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Error al actualizar el paciente: {str(e)}', 'danger')

        return redirect(url_for('expedientes'))

@app.route('/expedientes')
def expedientes():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id_paciente, nombre_med, paciente, fecha_nac, enfermedades_cronicas, alergias, antecedentes_familiares FROM tb_pacientes')
    pacientes = cursor.fetchall()
    return render_template('expedientes.html', pacientes=pacientes)

@app.route('/eliminarPaciente/<int:id>', methods=['POST'])
def eliminarPaciente(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM tb_pacientes WHERE id_paciente = %s', (id,))
        mysql.connection.commit()
        flash('Paciente eliminado correctamente')
    except Exception as e:
        flash('Error al eliminar el paciente: ' + str(e), 'danger')
    
    return redirect(url_for('expedientes'))

@app.route('/buscar_expedientes', methods=['GET', 'POST'])
def buscar_expedientes():
    if request.method == 'POST':
        criterio = request.form['criterio']
        busqueda = request.form['busqueda']
        cursor = mysql.connection.cursor()

        if criterio == 'nombre':
            cursor.execute('SELECT * FROM tb_pacientes WHERE paciente LIKE %s', ('%' + busqueda + '%',))
        elif criterio == 'fecha':
            try:
                fecha = datetime.strptime(busqueda, '%Y-%m-%d')
                cursor.execute('SELECT * FROM tb_pacientes WHERE fecha_nac = %s', [fecha])
            except ValueError:
                flash('Formato de fecha inválido. Usa AAAA-MM-DD.', 'danger')
                return redirect(url_for('expedientes'))

        pacientes = cursor.fetchall()
        return render_template('expedientes.html', pacientes=pacientes)
    
    return redirect(url_for('expedientes'))


@app.route('/reimprimir_receta/<int:id>', methods=['GET'])
def reimprimir_receta(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tb_recetas WHERE id_receta=%s', [id])
    receta = cursor.fetchone()
    cursor.close()
    
    if receta:
        return render_template('reimprimir_receta.html', receta=receta)
    else:
        flash('Receta no encontrada', 'danger')
        return redirect(url_for('home'))


@app.route('/citas_previas', methods=['GET'])
def citas_previas():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tb_citas WHERE id_medico=%s', [session.get('id_roles')])
    citas = cursor.fetchall()
    cursor.close()
    
    return render_template('citas_previas.html', citas=citas)

@app.errorhandler(404)     
def paginando(e):
    return 'Página no encontrada', 404
     
if __name__ == '__main__':
    app.run(debug=True, port=7000)
