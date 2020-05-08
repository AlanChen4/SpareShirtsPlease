import getpass
import smtplib
import unittest
import warnings

from SpareShirtsPlease.utils import sheets
from SpareShirtsPlease.utils import url_scraper
from SpareShirtsPlease.utils import email_scraper
from SpareShirtsPlease.constants import *


def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return do_test


class SpareShirtsTests(unittest.TestCase):

    @ignore_warnings
    def test_spreadsheet(self):
        '''test access to spreadsheet'''
        sheet_info = sheets.get_spreadsheet(SHEET_ID, TEST_RANGE)
        self.assertEqual(type(sheet_info), list, f'{sheet_info}')

    @ignore_warnings
    def test_email(self):
        '''test access to email address'''
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()

        password = getpass.getpass('[Email Password *Hidden]:')
        login_attempt = str(mail.login('alanrths@gmail.com', password))
        login_status = 'Accepted' in login_attempt
        self.assertEqual(login_status, True, 'Failed Login')

    @ignore_warnings
    def test_url_scraper(self):
        '''test if urls are being returned'''
        test_url_scraper = url_scraper.scraper()
        status = test_url_scraper.guess_url('devada')
        self.assertEqual(status, 'https://www.devada.com', 'Failed Guess URL')

    @ignore_warnings
    def test_email_scraper(self):
        '''test if emails are being returned'''
        test_email_scraper = email_scraper.scraper()

        test_urls = ['https://www.Springboard.com//contact/']
        status = test_email_scraper.get_contact_email(test_urls, test=True)
        self.assertEqual(type(status), set, f'{status}')

    if __name__ == '__main__':
        unittest.main()

