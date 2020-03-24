import os
import re
import requests
import requests.exceptions

from collections import deque
from googlesearch import search
from user_agent import generate_user_agent


class email_scraper():

    def get_base_url(self, companies):
        '''
        returns lists of either the top result of
        the google search with contact page or
        a DNE
        '''
        results = []
        for company_name in companies:
            companies_generator = search(
                query=company_name + ' contact',
                num=3,
                stop=1,
                pause=2)
            company_url = [url for url in companies_generator][0]

            # get the html of the contact page for company url
            session = requests.Session()
            session.headers.update({'User-Agent': generate_user_agent(
                device_type='desktop',
                os=('mac', 'linux'))})
            contact_page = session.get(url=company_url)

            if contact_page.status_code >= 200:
                results.append({company_name: company_url})
            else:
                results.append({company_name: 'DNE'})

        self.add_collected_urls(results)

    def add_collected_urls(self, urls):
        '''adds urls to text file under data/scraped'''
        index = self.create_directory('../data/scraped/collected_urls')
        path_name = '../data/scraped/collected_urls' + index + '/data.txt'
        with open(path_name, 'w+') as f:
            for url in urls:
                f.write(f'{url}\n')
            print(f'[finished]{len(urls)} urls added')

    def get_contact_email(self, list_of_urls):
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
        self.add_collected_emails(collected_emails)

    def add_collected_emails(self, emails):
        '''adds emails to text file under data/scraped'''
        index = self.create_directory('../data/scraped/collected_emails')
        path_name = '../data/scraped/collected_emails' + index + '/data.txt'
        with open(path_name, 'w+') as f:
            for email in emails:
                f.write(f'{email}\n')
            print(f'[finished]{len(emails)} emails added')

    def create_directory(self, path_name):
        '''creates new directory and adds index if duplicate'''
        index = ''
        while True:
            try:
                os.makedirs(path_name + index)
                break
            except WindowsError:
                if index:
                    # Append 1 to number in brackets
                    index = '(' + str(int(index[1:-1]) + 1) + ')'
                else:
                    index = '(1)'
                # Go and try create file again
                pass
        return index


if __name__ == '__main__':
    e_s = email_scraper()
    e_s.get_base_url(['duke admissions', 'devada'])
