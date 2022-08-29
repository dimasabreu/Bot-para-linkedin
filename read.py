from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd

# criando as credenciais necessarias para editar a sheet
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID spreadsheet.
SAMPLE_SPREADSHEET_ID = '1-Xmk4Rutb1i6YZt6hoIcg0hsDSYdhGzJmzoEF9cXRWQ'



def main():
   
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Acompanhamento!C1:BK11").execute()
    values = result.get('values', [])
    df = pd.DataFrame(values)
    print(df)
    
if __name__ == '__main__':
    main()