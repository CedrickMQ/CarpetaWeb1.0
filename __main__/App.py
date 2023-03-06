from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Email = request.form['Email']
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('inicio'))
    return render_template('index.html')

@app.route('/templates/index.html')
def inicio():
    return render_template('index.html')

@app.route('/templates/login.html')
def login():
    return render_template('login.html')

@app.route('/static/Sql/Login.php')
def loginPhp():
    return render_template('Login.php')

if __name__ == '__main__':
    app.run(debug= True, port=4000, host="0.0.0.0")