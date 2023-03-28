from flask import Flask, render_template, request, redirect, url_for,flash, session, send_file
from config import database

app = Flask(__name__)

app.secret_key = "NUT_NUT"

@app.route('/')
def index():
    return redirect(url_for('inicio'))

@app.route('/templates/index.html', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        return render_template ('index.html')
    else:
        return render_template ('index.html')

@app.route('/templates/login.html',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['Usuario']
        contrasena = request.form['password']
        cursor = database.cursor()
        cursor.execute('SELECT * FROM Usuarios_v2 WHERE Usuario = %s AND Contraseña = %s', (usuario, contrasena))
        cuenta = cursor.fetchone()
        if cuenta:
            session['Usuario'] = cuenta[1]
            flash ('Bienvenido')
            return redirect(url_for('inicio'))
        else:
            return render_template('login.html', error='Usuario o contraseña incorrecta.')
    else:
        return render_template('login.html')

@app.route('/templates/Formulario.html',methods=['GET', 'POST'])
def Registro():
    return render_template ('Formulario.html')

@app.route('/Formulario', methods=['GET','POST'])
def Form():
    if request.method == 'POST':

        Usuario = request.form['Usuario']
        Password = request.form['password']
        Fullname = request.form['Nombre']

        cursor = database.cursor(dictionary=True)
        cursor.execute('INSERT INTO Usuarios_v2 (Usuario, Contraseña, NombreCompleto) VALUES (%s, %s, %s);', (Usuario,Password,Fullname))
        database.commit()
        return redirect(url_for('Registro'))
    else:
        return redirect(url_for('Registro'))

if __name__ == '__main__':
    app.run(debug= True, port=4000, host="0.0.0.0")