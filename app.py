from flask import Flask, render_template, request, redirect, session
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = "segredo_super_secreto"

# ---------------- AUTH ----------------
import os

def carregar_usuarios():
    users_json = os.environ.get("USERS_JSON")
    if not users_json:
        raise Exception("USERS_JSON não configurado no Railway")
    return json.loads(users_json)


# ---------------- GOOGLE SHEETS ----------------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

import os

creds_json = os.environ.get("GOOGLE_CREDENTIALS")

if not creds_json:
    raise Exception("GOOGLE_CREDENTIALS não configurado no Railway")

creds_dict = json.loads(creds_json)

creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open("CRM Clientes").sheet1


# ---------------- ROTAS ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = carregar_usuarios()
        user = request.form["username"]
        password = request.form["password"]

        if user in users and users[user] == password:
            session["user"] = user
            return redirect("/")
        else:
            return "Login inválido"

    return render_template("login.html")


@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        email = request.form["email"]

        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        sheet.append_row([
    "",                 # A - ID
    nome,              # B - Nome
    telefone,         # C - Telefone
    email,            # D - Email
    "Novo",           # E - Status
    session["user"], # F - Usuário
    "",               # G - Observação
    now               # H - Data
])


        return redirect("/")

    return render_template("index.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

