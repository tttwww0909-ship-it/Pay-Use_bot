import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
'service_account.json',
scope
)

client = gspread.authorize(creds)

sheet = client.open("Pay&UsetgBot").sheet1

print(sheet.get_all_records())