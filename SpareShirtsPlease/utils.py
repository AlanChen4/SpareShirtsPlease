import getpass
import json
import pickle
import os.path
import smtplib

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# global variables
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def get_spreadsheet(sheet_ID, range_name):
	'''returns the desired spreadsheet information'''

	final_sheet = []
	creds = None
	# the file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
	    with open('token.pickle', 'rb') as token:
	        creds = pickle.load(token)
	# if there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
	    if creds and creds.expired and creds.refresh_token:
	        creds.refresh(Request())
	    else:
	        flow = InstalledAppFlow.from_client_secrets_file(
	            'data/credentials.json', SCOPES)
	        creds = flow.run_local_server(port=0)
	    # save the credentials for the next run
	    with open('token.pickle', 'wb') as token:
	        pickle.dump(creds, token)

	service = build('sheets', 'v4', credentials=creds)
	# call the Sheets API
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=sheet_ID,
	                            range=range_name).execute()
	values = result.get('values', [])

	if not values:
	    print('No data found.')
	else:
	    for row in values:
	        final_sheet.append(row)

	# converts lists of lists into a flattened list
	return [list_email[0] for list_email in final_sheet]


def load_email():
	'''gathers necessary information about email using email.json and email_body.txt'''
	with open('data/email.json') as email_file:
		email_info = json.load(email_file)
		email_subject = email_info['subject']

	email_body = open('data/email_body.txt').read()
	return email_subject, email_body


def send_emails(username, recipient_list):
	'''loops through recipient list and sends email to each one'''

	mail = smtplib.SMTP('smtp.gmail.com', 587)
	mail.ehlo()
	mail.starttls()

	password = getpass.getpass('[Email Password *Hidden]:')
	mail.login(username, password)

	subject, body = load_email()

	for recipient in recipient_list:
		message = f'To: {recipient}\r\nSubject: {subject}\r\n\r\n{body}'
		mail.sendmail(username, [recipient], message)
		print(f'SENT EMAIL TO {recipient}')

	print('FINISHED SENDING EMAILS')
	mail.close()

