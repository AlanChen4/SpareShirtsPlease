from utils import email_sender, scraper, sheets
from constants import *


class SpareShirtsPlease():

    def __init__(self):
        '''sets up the spreadsheets, email_sender, and tracker'''
        self.setup_spreadsheet()
        self.setup_email()

    def setup_spreadsheet(self):
        self.recipient_list = sheets.get_spreadsheet(SHEET_ID, TEST_RANGE)

    def setup_email(self):
        email_sender.send_emails(USERNAME, self.recipient_list)


def main():
    SpareShirtsPlease()


if __name__ == '__main__':
    main()
