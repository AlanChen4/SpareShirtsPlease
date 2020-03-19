import re
import requests
import requests.exceptions

from bs4 import BeautifulSoup
from googlesearch import search
from urllib.parse import urlsplit
from collections import deque


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


def find_contact_email(list_of_urls):
    '''
    uses simple crawler to extract
    email addresses from web page
    '''
    to_crawl = deque(list_of_urls)
    crawled = set()
    collected_emails = set()

    while len(to_crawl):
        # url is the current url that is being crawled
        url = to_crawl.popleft()
        crawled.add(url)

        # find base url and path for relative links
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url

        # gather page content from url
        print(f'Crawling {url}')
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        try:
            page_content = session.get(url=url)
            print(f'[{page_content.status_code}]{url}')
        except (requests.exceptions.MissingSchema,
                requests.exceptions.ConnectionError):
            print(f'[request failed]{url}')
            continue

        # extract all email addresses and add them into the resulting set
        new_emails = set(re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",
            page_content.text,
            re.I))
        print('new emails', new_emails)
        collected_emails.update(new_emails)

        soup = BeautifulSoup(page_content.text, features='lxml')

        # find and process all the anchors in the document
        for anchor in soup.find_all("a"):
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            # resolve relative links
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            # if link was not enqueued nor processed yet
            if link not in to_crawl and link not in crawled:
                to_crawl.append(link)

    print(f'collected emails {collected_emails}')
    print(f'number of collected emails {len(collected_emails)}')


if __name__ == '__main__':
    # find_contact_email(get_base_url('devada'))
    find_contact_email(
        ['https://admissions.duke.edu/contact/'])
