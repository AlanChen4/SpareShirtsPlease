import getpass
import json
import smtplib


def load_email():
    '''
    gathers necessary information about
    email using email.json and email_body.txt
    '''
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
