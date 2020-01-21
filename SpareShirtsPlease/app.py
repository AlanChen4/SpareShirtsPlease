import _utils

from constants import *

class SpareShirtsPlease():

	def __init__(self):
		self.sheet = _utils.get_spreadsheet(SHEET_ID, RANGE_NAME)
		print(self.sheet)

def main():
	s = SpareShirtsPlease()

if __name__ == '__main__':
	main()