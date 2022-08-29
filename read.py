from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from tkinter import *
import tkinter as tk

# iniciando o looping
root = tk.Tk()
root.title('Login Page')


# tamanho do monitor que acessou o programa
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# tamanho da tela do app
app_width = 350
app_height = 600

# pegando o ponto da tela pra por o app
x = (screen_width / 2) - (app_width / 2) 
y = (screen_height / 2) - (app_height / 2)
# parte de geometria q determina onde o app aparece na tela do usuario
root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

page_frame = tk.Frame(root)

# img do botao
s_face = '🙉'
h_face = '🙈'

# func para mostrar a senha
def showhide_pass():
    if pass_entry['show'] == '*':
        pass_entry.configure(show='')
        shide_btn.configure(text=s_face)
    else:
        pass_entry.configure(show='*')
        shide_btn.configure(text=h_face)


# 1 entrada de dados
email_lb = tk.Label(page_frame, text='Email', font=('Bold', 15))
email_lb.pack(pady=10)
udl_email = tk.Label(page_frame, text='———————————', font=('Bold', 15), fg='#d6d6d6')
udl_email.place(x=12, y=68)
email_entry = tk.Entry(page_frame, font=('Bold', 15), bd=0)
email_entry.pack(pady=10)
email_entry.bind("<FocusIn>", lambda e: udl_email.configure(fg='#0A66C2'))
email_entry.bind("<FocusOut>", lambda e: udl_email.configure(fg='#d6d6d6'))

# 2 entrada de dados
pass_lb = tk.Label(page_frame, text='Password', font=('Bold', 15))
pass_lb.pack(pady=10)
udl_pass = tk.Label(page_frame, text='———————————', font=('Bold', 15), fg='#d6d6d6')
udl_pass.place(x=12, y=163)
pass_entry = tk.Entry(page_frame, font=('Bold', 15), bd=0, show='*')
pass_entry.pack(pady=10)
pass_entry.bind("<FocusIn>", lambda e: udl_pass.configure(fg='#0A66C2'))
pass_entry.bind("<FocusOut>", lambda e: udl_pass.configure(fg='#d6d6d6'))

# mostrando a senha
shide_btn = tk.Button(root, text=h_face, font=('Bold', 15), bd=0, command=showhide_pass)
shide_btn.place(x= 290, y=166)



def linkedin():

    # criando as credenciais necessarias para editar a sheet
    SERVICE_ACCOUNT_FILE = 'keys.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)


    # The ID spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1-Xmk4Rutb1i6YZt6hoIcg0hsDSYdhGzJmzoEF9cXRWQ'



    def sheet():
        service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
        sheet = service.spreadsheets()
        # Escolhi a sheet e as linhas / colunas
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range="Acompanhamento!C2:BK2").execute()
        # Pegando o valor de dentro das colunas
        values = result.get('values', [])
        return values
        

    def cleandata():
        # criando um df
        df = pd.DataFrame(sheet())
        # transpondo as linhas para colunas
        df = df.T
        # dando um nome a coluna
        df.columns = ['Linkedin']
        df['Linkedin'].replace('', np.nan, inplace=True)
        df.dropna(subset=['Linkedin'], inplace=True)
        # limpando os links
        linkedola = []
        for link in df['Linkedin']:
            variavel_split = link.split(':')
            if variavel_split[0] == 'https':
                linkedola.append(link)
        return linkedola


    # criando o bot
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.linkedin.com')
    time.sleep(2)
    # logando na sua conta do linkedin
    username = driver.find_element(By.XPATH, "//input[@name='session_key']")
    username.send_keys(email_entry.get())
    password = driver.find_element(By.XPATH, "//input[@name='session_password']")
    password.send_keys(pass_entry.get())
    time.sleep(2)
    submit = driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    # mudando a pagina 

    links = cleandata()
    for element in links:
        # colocando os linkedins na tela
        driver.get(element)
        time.sleep(2)
        # procurando todos os botoes da tela
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        # testando todos ate achar o botao de conectar correto
        for button in all_buttons:
            if button.text == "Conectar":
                try:
                    button.click()
                    time.sleep(2)
                    nota = driver.find_element(By.XPATH, "//button[@aria-label='Adicionar nota']")
                    nota.click()
                    time.sleep(2)
                    texto = driver.find_element(By.ID, "custom-message").send_keys("Olá, fazemos parte da mentoria conquiste sua vaga!")
                    time.sleep(2)
                    adicionar = driver.find_element(By.XPATH, "//button[@aria-label='Enviar agora']")
                    adicionar.click()
                    time.sleep(2)
                    pass
                except:
                    break
        

# botao de envio
login_btn = tk.Button(page_frame, text='Login', font=('Bold', 15), bd=0, bg='#0A66C2', fg='white', width=20, command=linkedin)
login_btn.pack(pady=20)

page_frame.pack(pady=20)
page_frame.pack_propagate(False)
page_frame.configure(width=250, height=500)



root.mainloop()