import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import time


def find_min(lst):
    # O(N) time complexity
    min_val = None
    min_dct = None
    for dct in lst:
        if min_val is None or float(dct['ACCURACY:']) < min_val:
            min_val = float(dct['ACCURACY:'])
            min_dct = dct
    return min_dct

start = time.time()

scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",scope)

client = gspread.authorize(creds)

sheet = client.open("TRC - Data").sheet1

data = sheet.get_all_records()

end = time.time()

print(end - start)

print(find_min(data))


