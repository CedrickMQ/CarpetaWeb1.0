from flask import Flask, render_template, request, redirect, url_for,flash, session, send_file
from config import database
import json

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os
import smtplib


path_pdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"

app = Flask(__name__)

app.secret_key = "NUT_NUT"

@app.route('/')
def index():
    return redirect(url_for('inicio'))

@app.route('/templates/index.html', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        usuario = request.form['Usuario']
        contrasena = request.form['password']
        cursor = database.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE Nickname = %s AND Contraseña = %s', (usuario, contrasena))
        cuenta = cursor.fetchone()
        basura = cursor.fetchall()
        if cuenta:
            session['Usuario'] = cuenta[1]
            if cuenta[4] == "admin":
                return redirect(url_for('Administracion'))
            else:
                return redirect(url_for('inicioControl'))
        else:
            return render_template('login.html', error='Usuario o contraseña incorrecta.')
    else:
        return render_template('index.html')

@app.route('/templates/login.html',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['Usuario']
        contrasena = request.form['password']
        cursor = database.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE Nickname = %s AND Contraseña = %s', (usuario, contrasena))
        cuenta = cursor.fetchone()
        basura = cursor.fetchall()
        if cuenta:
            session['Usuario'] = cuenta[1]
            if cuenta[4] == "admin":
                return redirect(url_for('Administracion'))
            else:
                return redirect(url_for('inicioControl'))
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
        cursor.execute('INSERT INTO Usuarios (Nickname, Contraseña, Nombre) VALUES (%s, %s, %s);', (Usuario,Password,Fullname))
        database.commit()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('Registro'))
    
@app.route('/templates/Admon.html')
def Administracion():
    cursor = database.cursor()
    cursor.execute("SELECT citas.idCitas, Doctores.nombre as NombreDoc, citas.Dia_semana FROM citas JOIN Doctores ON citas.Doctores_idDoctores = doctores.idDoctores;")
    data = cursor.fetchall()
    return render_template('Admon.html', data=data)
    

@app.route('/templates/Control.html')
def inicioControl():
    cursor = database.cursor()
    cursor.execute("SELECT citas.idCitas, Doctores.nombre as NombreDoc, citas.Dia_semana FROM citas JOIN Doctores ON citas.Doctores_idDoctores = doctores.idDoctores;")
    data = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM citas;")
    HayDatos = cursor.fetchone()

    if HayDatos is not None:
        valor_t = HayDatos[0]
        valor = int(valor_t)
    else:
        valor = 0

    if valor == 0:
        data = "No tiene citas"

    cursor.execute("SELECT COUNT(*) FROM `Citas` WHERE `dia_semana` = 'lunes';")
    D_Lunes = cursor.fetchone()
    if D_Lunes is not None:
        valor_t = D_Lunes[0]
        Di_Lunes = int(valor_t)
    else:
        Di_Lunes = 0
    return render_template ('Control.html', data=data , Di_Lunes=Di_Lunes)

@app.route('/GeneradorCitas',methods=['GET','POST'])
def GenerarCita():
    if request.method == 'POST':

        usuario = '1'
        DCita = request.form['Dia']
        Doc = request.form['NombreDoc']

        cursor = database.cursor(dictionary=True)
        cursor.execute('INSERT INTO citas (Doctores_idDoctores, Usuarios_id, Dia_semana) VALUES (%s, %s, %s);', (Doc, usuario ,DCita))
        database.commit()
        return redirect(url_for('inicioControl'))
    else:
        return redirect(url_for('inicioControl'))
    
def crear_pdf():
    # Crear un archivo PDF con ReportLab
    cursor = database.cursor()

    # Ejecutar consulta para obtener los datos de la tabla
    query = 'SELECT citas.idCitas, Doctores.nombre as NombreDoc, citas.Dia_semana FROM citas JOIN Doctores ON citas.Doctores_idDoctores = doctores.idDoctores;'
    cursor.execute(query)
    datos = cursor.fetchall()

    # Crear el archivo PDF con ReportLab
    archivo_pdf = SimpleDocTemplate("ejemplo.pdf", pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30,
                                    bottomMargin=18)
    tabla_datos = []

    # Añadir los encabezados de la tabla
    encabezados = ("ID", "Nombre", "Dia")
    tabla_datos.append(encabezados)

    # Añadir los datos de la tabla a la lista de datos
    for dato in datos:
        tabla_datos.append(dato)

    # Crear la tabla
    tabla = Table(tabla_datos, colWidths=[2 * inch, 2 * inch, 2 * inch])

    # Agregar estilos a la tabla
    estilo = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                         ('FONTSIZE', (0, 0), (-1, 0), 14),
                         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                         ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                         ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                         ('FONTSIZE', (0, 1), (-1, -1), 12),
                         ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                         ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    tabla.setStyle(estilo)

    # Añadir la tabla al archivo PDF y cerrarlo
    elementos = []
    elementos.append(tabla)
    archivo_pdf.build(elementos)
    cursor.close()

def enviarCorreos():
    sender_email = 'cedrick.marcial25@unach.com'
    sender_password = 'tu_contraseña'
    receiver_email = 'correo_destino@gmail.com'

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)

        subject = 'Prueba de correo desde Flask'
        body = 'Este es un correo de prueba enviado desde Flask.'

        message = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(sender_email, receiver_email, message)

    return 'Correo enviado'

@app.route('/pdf')
def Gatillo_pdf():
    crear_pdf()
    path = os.path.abspath("ejemplo.pdf")
    return send_file(path,'ejemplo.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug= True, port=4000, host="0.0.0.0")