import os
from flask import Flask, request, render_template, url_for, redirect, flash
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdflask'
app.secret_key = 'mysecretkey'

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

mysql = MySQL(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM albums')
        consultaA = cursor.fetchall()
        return render_template('index.html', albums=consultaA)
    except Exception as e:
        print(e)
        flash('Error al cargar los datos')
        return render_template('index.html', albums=[])

@app.route('/eliminar/<id>')
def eliminar(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM albums WHERE idAlbum = %s', (id,))
        mysql.connection.commit()
        flash('Album eliminado correctamente')
    except Exception as e:
        print(e)
        flash('Error al eliminar el album')
    return redirect(url_for('index'))

@app.route('/editar/<id>')
def editar(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM albums WHERE idAlbum=%s', [id])
        albumE = cur.fetchone()
        return render_template('editar.html', album=albumE)
    except Exception as e:
        print(e)
        flash('Error al cargar el album para edición')
        return redirect(url_for('index'))

@app.route('/guardarCambios/<id>', methods=['POST'])
def guardarCambios(id):
    if request.method == 'POST':
        ftitulo = request.form['txtTitulo']
        fartista = request.form['txtArtista']
        fanio = request.form['txtAnio']
        cursor = mysql.connection.cursor()

        if 'portada' in request.files:
            file = request.files['portada']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                fportada = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                cursor.execute('UPDATE albums SET titulo=%s, artista=%s, anio=%s, portada=%s WHERE idAlbum=%s', 
                               (ftitulo, fartista, fanio, fportada, id))
                mysql.connection.commit()
                flash('Cambios guardados correctamente')
                return redirect(url_for('index'))

        cursor.execute('UPDATE albums SET titulo=%s, artista=%s, anio=%s WHERE idAlbum=%s', 
                       (ftitulo, fartista, fanio, id))
        mysql.connection.commit()
        flash('Cambios guardados correctamente')
        return redirect(url_for('index'))

@app.route('/guardarAlbum', methods=['POST'])
def guardarAlbum():
    if request.method == 'POST':
        ftitulo = request.form['txtTitulo']
        fartista = request.form['txtArtista']
        fanio = request.form['txtAnio']
        cursor = mysql.connection.cursor()

        if 'portada' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['portada']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fportada = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            cursor.execute('INSERT INTO albums (titulo, artista, anio, portada) VALUES (%s, %s, %s, %s)', 
                           (ftitulo, fartista, fanio, fportada))
            mysql.connection.commit()
            flash('¡¡Album guardado correctamente!!')
            return redirect(url_for('index'))

@app.errorhandler(404)
def paginando(e):
    return 'revisa tu sintaxis: no encontrado naada'

if __name__ == '__main__':
    app.run(debug=True, port=3000)
