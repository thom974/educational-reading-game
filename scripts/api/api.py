# IMPORTS --------------------------
import gspread
import pygame
from oauth2client.service_account import ServiceAccountCredentials
from urllib.request import Request, urlopen
import requests
import io
from pprint import pprint
# INIT -----------------------------
pygame.init()

class Spreadsheet:
    def __init__(self):
        # the worksheet itself
        self.database = None
        self.active_row = None

        # instance variables for 'Word Mode'
        self.active_word = None
        self.incorrect_words = []
        self.word_history = []

        # instance variables for 'Visual Mode'
        self.active_picture_link = ""
        self.image_surface = None

    def fetch_endpoint(self,num):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("scripts/api/credentials.json", scope)
        client = gspread.authorize(creds)
        self.database = client.open("TRC - Data").get_worksheet(num)

    # 'Word Mode' methods below
    def find_min(self):
        # O(N) time complexity
        lst = self.database.get_all_records()
        min_val, min_dct = None, None

        for row_num, dct in enumerate(lst):
            if (min_val is None or float(dct['ACCURACY:']) < min_val) and dct['WORD:'] not in self.incorrect_words:
                min_val = float(dct['ACCURACY:'])
                min_dct = dct
                self.active_row = row_num + 2

        self.word_history.append(min_dct['WORD:'])
        self.active_word = min_dct['WORD:']

    # 'Visual Mode' methods below
    def find_picture_min(self):
        # O(N) time complexity
        lst = self.database.get_all_values()[1:]
        min_lst = lst[0]

        for row_num, row in enumerate(lst):
            if int(row[1]) <= int(min_lst[1]):
                min_lst = row
                self.active_row = row_num + 2

        self.active_picture_link = min_lst[0]

    def load_picture(self):
        # req = Request(
        #     self.active_picture_link,
        #     headers={'User-Agent': 'Mozilla/5.0'})
        # image_data = urlopen(req).read()
        # image_file = io.BytesIO(image_data)
        r = requests.get(self.active_picture_link)
        img = io.BytesIO(r.content)
        self.image_surface = pygame.image.load(img)

# if __name__ == '__main__':
#     s = Spreadsheet()
#     s.fetch_endpoint()
#     s.find_min()
#     print(s.active_word)



