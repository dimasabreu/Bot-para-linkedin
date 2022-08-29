from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


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
username = driver.find_element('xpath', "//input[@name='session_key']")
username.send_keys()
password = driver.find_element('xpath', "//input[@name='session_password']")
password.send_keys()
time.sleep(2)
submit = driver.find_element('xpath', "//button[@type='submit']").click()
time.sleep(2)  

if __name__ == '__main__':
    sheet()
    cleandata()
    