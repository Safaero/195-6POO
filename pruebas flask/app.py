from flask import Flask, request, render_template, url_for, redirect, flash, session
from flask_mysqldb import MySQL
<<<<<<< Updated upstream
=======
from functools import wraps
>>>>>>> Stashed changes

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdflask'
app.secret_key = 'mysecretkey'

<<<<<<< Updated upstream
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
=======
# Clave secreta para las sesiones
app.secret_key = 'mysecretkey'

mysql = MySQL(app)

# Decorador para proteger las rutas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Por favor, inicia sesión primero.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta para el inicio de sesión
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
>>>>>>> Stashed changes
def login():
    if request.method == 'POST':
        rfc = request.form['rfc']
        contraseña = request.form['contraseña']
<<<<<<< Updated upstream
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT nombre FROM tb_medicos WHERE rfc = %s AND contraseña = %s', (rfc, contraseña))
        medico = cursor.fetchone()
        
        if medico:
            session['nombre_medico'] = medico[0] 
            return redirect(url_for('home'))
        else:
            flash('Credenciales incorrectas. Inténtalo de nuevo.')
            return redirect(url_for('login'))
    return render_template('login.html')


=======

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_medicos WHERE rfc = %s AND contraseña = %s', (rfc, contraseña))
        user = cursor.fetchone()

        if user:
            session['logged_in'] = True
            session['user_id'] = user[0]  # Guarda el ID del usuario en la sesión
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('login'))
    return render_template('login.html')

# Ruta para la página principal
>>>>>>> Stashed changes
@app.route('/home')
@login_required
def home():
<<<<<<< Updated upstream
    nombre_medico = session.get('nombre_medico', 'Doctor')
    return render_template('index.html', nombre_medico=nombre_medico)
=======
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_medicos')
        consultaA = cursor.fetchall()
        return render_template('index.html', albums=consultaA)
    except Exception as e:
        print(f"Error al realizar la consulta en la tabla tb_medicos: {e}")
        return render_template('index.html', albums=[])
>>>>>>> Stashed changes

# Otras rutas protegidas
@app.route('/registros')
@login_required
def registros():
    return render_template('registros.html')

@app.route('/consulta')
@login_required
def consulta():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM tb_medicos')
    medicos = cursor.fetchall()
    return render_template('consulta.html', medicos=medicos)

<<<<<<< Updated upstream
        return render_template ('consulta.html',medicos=medicos)	
    

@app.route('/guardarMedico',methods=['POST'])
=======
@app.route('/expedientes')
@login_required
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
@login_required
def guardarPaciente():
    if request.method == 'POST':
        fnombre = request.form['txtnombre']
        fpaciente = request.form['txtpaciente']
        ffecha = request.form['txtfecha']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_medicos WHERE nombre = %s', (fnombre,))
        medico = cursor.fetchone()

        if medico is None:
            flash('El nombre del médico no existe en la tabla de médicos.')
            return redirect(url_for('expedientes'))

        cursor.execute('INSERT INTO tb_pacientes (nombre, paciente, fecha) VALUES (%s, %s, %s)', (fnombre, fpaciente, ffecha))
        mysql.connection.commit()
        flash('Expediente generado correctamente')
        return redirect(url_for('expedientes'))

@app.route('/guardarMedico', methods=['POST'])
@login_required
>>>>>>> Stashed changes
def guardarMedico():
    if request.method == 'POST':
        fnombre = request.form['txtnombre']
        fcorreo = request.form['txtcorreo']
        frol = request.form['txtrol']
        fcedula = request.form['txtcedula']
        frfc = request.form['txtrfc']
        fcontraseña = request.form['txtcontraseña']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO tb_medicos (nombre, correo, id_roles, cedula, rfc, contraseña) VALUES (%s, %s, %s, %s, %s, %s)', (fnombre, fcorreo, frol, fcedula, frfc, fcontraseña))
        mysql.connection.commit()
        flash('Médico integrado correctamente')
        return redirect(url_for('consulta'))
<<<<<<< Updated upstream
    
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
=======
>>>>>>> Stashed changes

@app.route('/editarPaciente/<int:id>', methods=['GET', 'POST'])
@login_required
def editarPaciente(id):
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        nombre_med = request.form['txtnombre_med']
        paciente = request.form['txtpaciente']
        fecha = request.form['txtfecha']

        cursor.execute("""
            UPDATE tb_pacientes 
            SET nombre_med = %s, paciente = %s, fecha = %s 
            WHERE id_paciente = %s
        """, (nombre_med, paciente, fecha, id))
        mysql.connection.commit()
        flash('Paciente actualizado correctamente')
        return redirect(url_for('expedientes'))
<<<<<<< Updated upstream

    cursor.execute('SELECT * FROM tb_pacientes WHERE id_paciente = %s', (id,))
    paciente = cursor.fetchone()
    return render_template('editar_paciente.html', paciente=paciente)
    
@app.route('/expedientes')
def expedientes():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id_paciente, nombre_med, paciente, fecha FROM tb_pacientes')
    pacientes = cursor.fetchall()
    return render_template('expedientes.html', pacientes=pacientes)

@app.route('/eliminarPaciente/<int:id>')
=======
    else:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_pacientes WHERE id=%s', (id,))
        paciente = cursor.fetchone()
        return render_template('editar_paciente.html', paciente=paciente)

@app.route('/eliminarPaciente/<int:id>', methods=['GET', 'POST'])
@login_required
>>>>>>> Stashed changes
def eliminarPaciente(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM tb_pacientes WHERE id_paciente = %s', (id,))
    mysql.connection.commit()
    flash('Paciente eliminado correctamente')
    return redirect(url_for('expedientes'))

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('Has cerrado sesión correctamente.')
    return redirect(url_for('login'))

# Manejo de errores 404
@app.errorhandler(404)     
def paginando(e):
    return 'Sintaxis incorrecta'

if __name__ == '__main__':
    app.run(debug=True, port=7000)
<<<<<<< Updated upstream
    
=======
>>>>>>> Stashed changes
