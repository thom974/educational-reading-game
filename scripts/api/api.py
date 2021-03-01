import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

class Spreadsheet:
    def __init__(self):
        self.database = None
        self.active_word = None
        self.active_row = None
        self.incorrect_words = []

    def fetch_endpoint(self):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("scripts/api/credentials.json", scope)
        client = gspread.authorize(creds)
        self.database = client.open("TRC - Data").sheet1

    def find_min(self):
        # O(N) time complexity
        lst = self.database.get_all_records()
        min_val, min_dct = None, None

        for row_num, dct in enumerate(lst):
            if (min_val is None or float(dct['ACCURACY:']) < min_val) and dct['WORD:'] not in self.incorrect_words:
                min_val = float(dct['ACCURACY:'])
                min_dct = dct
                self.active_row = row_num + 2

        self.active_word = min_dct['WORD:']

# if __name__ == '__main__':
#     s = Spreadsheet()
#     s.fetch_endpoint()
#     s.find_min()
#     print(s.active_word)



