import _utils

from constants import *

class SpareShirtsPlease():

	def setup_all(self):
		'''sets up the spreadsheets, email, and tracker'''
		self.setup_spreadsheet()
		self.setup_email()
		self.setup_tracker()


	def setup_spreadsheet(self):
		self.recipient_list = _utils.get_spreadsheet(SHEET_ID, TEST_RANGE)


	def setup_email(self):
		_utils.send_emails(recipient_list=self.recipient_list, test=True)


	# TODO: this feature may or may not be added
	def setup_tracker(self):
		pass


def main():
	s = SpareShirtsPlease()
	s.setup_all()

if __name__ == '__main__':
	main()