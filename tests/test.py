import getpass
import smtplib
import unittest
import warnings

from SpareShirtsPlease.utils import sheets
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
		login_status = 'Accepted' in str(mail.login('alanrths@gmail.com', password))
		self.assertEqual(login_status, True, 'Failed Login')

if __name__ == '__main__':
	unittest.main()