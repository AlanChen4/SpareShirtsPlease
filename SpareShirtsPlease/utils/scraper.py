import numpy as np
import multiprocessing as mutli
import os
import re
import requests
import requests.exceptions

from bs4 import BeautifulSoup
from multiprocessing import Manager
from user_agent import generate_user_agent


def chunks(n, page_list):
    '''
    splits the list into n chunks
    used for multiprocessing
    '''
    return np.array_split(page_list, n)


class email_url_scraper():

    def get_base_url(self, companies):
        '''
        returns lists of either the top result of
        the google search with contact page or
        a DNE
        '''
        with Manager() as manager:
            cpus = mutli.cpu_count()
            workers = []
            company_bins = chunks(cpus, companies)
            collected_urls = manager.list()

            for cpu in range(cpus):
                worker = mutli.Process(
                    name=str(cpu),
                    target=self.get_contact_page,
                    args=(company_bins[cpu], collected_urls,))

                worker.start()
                workers.append(worker)

            for worker in workers:
                worker.join()

            self.add_collected_urls(collected_urls)

    def get_contact_page(self, list_of_names, collected_urls):
        '''
        gets the link to the contact page
        '''
        for name in list_of_names:
            company_url = self.guess_url(name)

            # get the html of the contact page for company url
            session = requests.Session()
            session.headers.update({'User-Agent': generate_user_agent(
                device_type='desktop',
                os=('mac', 'linux'))})
            try:
                resp = session.get(url=company_url)
                soup = BeautifulSoup(
                    resp.text,
                    features='lxml')

                for link in soup.find_all('a', href=True):
                    if 'contact' in link['href']:
                        final_url = company_url + '/' + link['href']

                        print(final_url)
                        collected_urls.append(final_url)
            except requests.exceptions.RequestException as e:
                print(f'{name}: {e}')

    def guess_url(self, name):
        '''
        try and guess the company url as this
        method is faster than performing google search
        query
        '''
        domains = ['.com', '.net', '.io', '.org', '.co']
        for domain in domains:
            try:
                url_guess = 'https://www.' + name + domain
                attempt = requests.head(
                    url=url_guess,
                    headers={'User-Agent': generate_user_agent(
                        device_type='desktop',
                        os=('mac', 'linux'))},
                    allow_redirects=True,
                    timeout=5)
                print(attempt, url_guess)
                if attempt.status_code >= 200:
                    return url_guess
            except requests.exceptions.ConnectionError:
                continue
            except requests.exceptions.ReadTimeout:
                continue

    def add_collected_urls(self, collected_urls):
        '''
        adds urls to text file under data/scraped
        '''
        index = self.create_directory('../data/scraped/collected_urls')
        path_name = '../data/scraped/collected_urls' + index + '/data.txt'
        with open(path_name, 'w+') as f:
            for url in collected_urls:
                f.write(f'{url}\n')
            print(f'[finished]{len(collected_urls)} urls added')

    def get_contact_email(self, list_of_urls):
        '''
        uses simple crawler to extract
        email addresses from web page
        '''
        session = requests.Session()
        session.headers.update({'User-Agent': generate_user_agent(
            device_type='desktop',
            os=('mac', 'linux'))})

        collected_emails = []

        for url in list_of_urls:
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
            collected_emails.append({url: new_emails})

        self.add_collected_emails(collected_emails)

    def add_collected_emails(self, emails):
        '''
        adds emails to text file under data/scraped
        '''
        index = self.create_directory('../data/scraped/collected_emails')
        path_name = '../data/scraped/collected_emails' + index + '/data.txt'
        with open(path_name, 'w+') as f:
            for email in emails:
                f.write(f'{email}\n')
            print(f'[finished]{len(emails)} emails added')

    def create_directory(self, path_name):
        '''
        creates new directory and adds index if duplicate
        '''
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


def main():
    e_s = email_url_scraper()
    e_s.get_base_url(['certipath', 'devada'])


if __name__ == '__main__':
    main()
