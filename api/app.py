from flask import Flask, render_template, redirect, request
from auth import login

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/inregistrare')
def inregistrare():
    return render_template('inregistrare.html')

@app.route('/autentificare', methods=["POST"])
def autentificare():
    email = request.form['email']
    password = request.form['password']
    return redirect("/inregistrare") if not login(email, password) else redirect('/')
