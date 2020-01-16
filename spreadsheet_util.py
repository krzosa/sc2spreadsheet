import gspread
import configuration
from oauth2client.service_account import ServiceAccountCredentials

def getGoogleSheetObject():
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client.json', scope)
    client = gspread.authorize(creds)
    return client.open("Starcraft2Spreadsheet").sheet1