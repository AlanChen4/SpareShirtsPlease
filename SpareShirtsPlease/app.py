import _utils

from constants import *


class SpareShirtsPlease():

	def __init__(self):
		'''sets up the spreadsheets, email, and tracker'''
		self.setup_spreadsheet()
		self.setup_email()
		self.setup_tracker()


	def setup_spreadsheet(self):
		self.recipient_list = _utils.get_spreadsheet(SHEET_ID, TEST_RANGE)


	def setup_email(self):
		_utils.send_emails(recipient_list=self.recipient_list)


	def setup_tracker(self):
		pass


def main():
	s = SpareShirtsPlease()

if __name__ == '__main__':
	main()