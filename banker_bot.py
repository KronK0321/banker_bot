import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('banker-bot-be73f3796456.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open("test sheet").sheet1
sht1 = gc.open_by_key('1OZE3X0pDjxkeYg5AQWB9aH-j2g3GyR79jdSzB7ue-n4')

worksheet = sht1.sheet1
val = worksheet.acell('A1').value

print(val)
worksheet.update_acell('B1', 'Bingo!')
