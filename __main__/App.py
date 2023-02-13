from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
#    
#@app.route('/Especialidades.html')
#def Especialidades():
#    return render_template('Especialidades.html')

#@app.route('/Servicios.html')
#def Servicios():
#    return render_template('Servicios.html')

#@app.route('/Quienes Somos.html')
#def Quienes_Somos():
#    return render_template('Quienes Somos.html')

#@app.route('/Contacto.html')
#def Contacto():
#    return render_template('Contacto.html')

#@app.route('/Sesion.html')
#def Sesion():
#    return render_template('Sesion.html')

if __name__ == '__main__':
    app.run(debug= True, port=4000, host="0.0.0.0")