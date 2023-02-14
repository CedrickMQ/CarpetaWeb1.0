from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/templates/login.html')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug= True, port=4000, host="0.0.0.0")