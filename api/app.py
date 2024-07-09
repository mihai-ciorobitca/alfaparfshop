from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/register')
def register():
    return render_template('register.html')