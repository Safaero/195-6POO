from flask import Flask, request, render_template, url_for, redirect, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdflask'
app.secret_key = 'mysecretkey'

mysql = MySQL(app)

from flask import Flask, request, render_template, url_for, redirect, flash, session
from flask_mysqldb import MySQL

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
        

        cursor.execute('SELECT nombre, id_roles FROM tb_medicos WHERE rfc = %s AND contraseña = %s', (rfc, contraseña))
        medico = cursor.fetchone()
        
        if medico:
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
        cursor= mysql.connection.cursor();
        cursor.execute('select * from tb_medicos')
        medicos= cursor.fetchall()

        return render_template ('consulta.html',medicos=medicos)	
    

@app.route('/guardarMedico', methods=['POST'])
def guardarMedico():
    if request.method == 'POST':
        # Obtener los datos del formulario
        fnombre = request.form['txtnombre']
        fcorreo = request.form['txtcorreo']
        frol = request.form['txtid_roles']
        fcedula = request.form['txtcedula']
        frfc = request.form['txtrfc']
        fcontraseña = request.form['txtcontraseña']

        try:
            cursor = mysql.connection.cursor()
            
            cursor.execute('''
                INSERT INTO tb_medicos (nombre, correo, id_roles, cedula, rfc, contraseña)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (fnombre, fcorreo, frol, fcedula, frfc, fcontraseña))
            

            mysql.connection.commit()
            cursor.close()
            

            flash('Médico guardado correctamente', 'success')
            
        except Exception as e:
            mysql.connection.rollback()
            flash('Error al guardar el médico: ' + str(e), 'danger')
        
        return redirect(url_for('registros'))

@app.route('/editarMedico/<id>')
def editarM(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tb_medicos WHERE id_medico=%s', [id])
    medico = cur.fetchone()
    cur.close()
    if medico:
        return render_template('editarMedico.html', medico=medico)
    else:
        flash('Médico no encontrado', 'danger')
        return redirect(url_for('index'))

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

            cursor = mysql.connection.cursor()
            cursor.execute('''
                           UPDATE tb_medicos 
                           SET nombre=%s, correo=%s, id_roles=%s, cedula=%s, rfc=%s, contraseña=%s 
                           WHERE id_medico=%s
                           ''', (fnombre, fcorreo, frol, fcedula, frfc, fcontraseña, id))

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
        fecha = request.form['txtfecha']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO tb_pacientes (nombre_med, paciente, fecha) VALUES (%s, %s, %s)', 
                       (nombre_med, paciente, fecha))
        mysql.connection.commit()
        flash('Paciente registrado correctamente')
        return redirect(url_for('expedientes'))

    
@app.route('/expedientes')
def expedientes():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id_paciente, nombre_med, paciente, fecha FROM tb_pacientes')
    pacientes = cursor.fetchall()
    return render_template('expedientes.html', pacientes=pacientes)

@app.route('/eliminarPaciente/<int:id>')
def eliminarPaciente(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM tb_pacientes WHERE id_paciente = %s', (id,))
    mysql.connection.commit()
    flash('Paciente eliminado correctamente')
    return redirect(url_for('expedientes'))

     
@app.errorhandler(404)     
def paginando(e):
    return 'sintaxis incorrecta'
     
if __name__ == '__main__':
    app.run(debug=True, port=7000)