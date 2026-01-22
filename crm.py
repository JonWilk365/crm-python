import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

sheet = client.open("CRM").sheet1

def adicionar_cliente(nome, telefone, email):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    sheet.append_row(["", nome, telefone, email, "Novo", "", "", now, "", ""])
    print("Cliente adicionado!")

adicionar_cliente("Cliente Teste", "11999999999", "teste@email.com")
