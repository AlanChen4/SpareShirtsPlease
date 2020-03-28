from utils import email_sender, url_scraper, sheets
from constants import *


class SpareShirtsPlease():

    def setup_spreadsheet(self):
        self.recipient_list = sheets.get_spreadsheet(SHEET_ID, BAY_AREA_RANGE)

    def setup_email(self):
        email_sender.send_emails(USERNAME, self.recipient_list)

    def setup_scraper(self):
        e_s = url_scraper.scraper()
        e_s.start(companies=self.recipient_list)


def main():
    s = SpareShirtsPlease()
    s.setup_spreadsheet()
    s.setup_scraper()


if __name__ == '__main__':
    main()
