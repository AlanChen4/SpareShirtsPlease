import re
import requests
import requests.exceptions

from bs4 import BeautifulSoup
from collections import deque
from googlesearch import search
from urllib.parse import urlsplit
from user_agent import generate_user_agent


class email_scraper():

    def get_base_url(self, company_name):
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
        session.headers.update({'User-Agent': generate_user_agent(
            device_type='desktop',
            os=('mac', 'linux'))})
        contact_page = session.get(url=company_url)

        if contact_page.status_code >= 200:
            return company_url
        else:
            return "DNE"

    def find_contact_email(self, list_of_urls):
        '''
        uses simple crawler to extract
        email addresses from web page
        '''
        session = requests.Session()
        session.headers.update({'User-Agent': generate_user_agent(
            device_type='desktop',
            os=('mac', 'linux'))})

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
            try:
                print(f'Crawling {url}')
                page_content = session.get(
                    url=url,
                    timeout=5)
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
            print(f'new emails {new_emails}')
            collected_emails.update(new_emails)

            # find and process all the anchors in the document
            soup = BeautifulSoup(page_content.text, features='lxml')
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


if __name__ == '__main__':
    e_s = email_scraper()

    # find_contact_email(get_base_url('devada'))
    e_s.find_contact_email(
        ['https://admissions.duke.edu/contact/'])
