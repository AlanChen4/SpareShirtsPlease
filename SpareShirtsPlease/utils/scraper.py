import requests

from bs4 import BeautifulSoup
from googlesearch import search


def get_base_url(company_name):
    '''
    returns either the top result of
    the google search with contact page or
    a DNE
    '''
    companies_generator = search(company_name, num=3, stop=1, pause=2)
    for url in companies_generator:
        company_url = url
    company_url += "/contact/"

    # get the html of the contact page for company url
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    contact_page = session.get(url=company_url)

    if contact_page.status_code >= 200:
        return company_url
    else:
        return "DNE"


def find_contact_email(url):
    '''
    uses simple crawler to extract
    email addresses from web page
    '''
    # soup = BeautifulSoup(response.text)


if __name__ == '__main__':
    print(get_base_url('devada'))
