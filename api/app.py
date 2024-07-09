from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/inregistrare')
def register():
    return render_template('inregistrare.html')