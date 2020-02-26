import requests

from bs4 import BeautifulSoup
from googlesearch import search


def find_contact_email(company_name):
    '''
    1. use name from spreadsheet
    2. google search result (maybe find way to choose from top 3)
    3. go to /contact part of site
    4. grab email address from page
    '''
    # make a guess at what company contact url is
    companies_generator = search(company_name, num=3, stop=1, pause=2)
    for url in companies_generator:
        company_url = url
    company_url += "/contact"

    # get the html of the contact page for company url
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    contact_page = session.get(url=company_url)

    soup = BeautifulSoup(contact_page.text, 'html.parser')
    print(soup.text)


if __name__ == '__main__':
    find_contact_email('devada')
