import numpy as np
import multiprocessing as multi
import os
import requests
import requests.exceptions

from bs4 import BeautifulSoup
from user_agent import generate_user_agent


def chunks(n, page_list):
    '''
    splits the list into n chunks
    used for multiprocessing
    '''
    return np.array_split(page_list, n)


class scraper:

    def start(self, companies):
        '''
        returns lists of either the top result of
        the google search with contact page or
        a DNE
        '''
        self.index, self.filepath = self.create_dir(
            path_name='../data/scraped/collected_urls')

        cpus = multi.cpu_count()
        workers = []
        company_bins = chunks(cpus, companies)

        for cpu in range(cpus):
            worker = multi.Process(
                name=str(cpu),
                target=self.get_contact_url,
                args=(company_bins[cpu],))

            worker.start()
            workers.append(worker)

    def get_contact_url(self, list_of_names):
        '''
        gets the link to the contact page
        '''
        session = requests.Session()
        session.headers.update({'User-Agent': generate_user_agent(
            device_type='desktop',
            os=('mac', 'linux'))})

        for name in list_of_names:
            company_url = self.guess_url(name)

            # get the html of the contact page for company url
            try:
                resp = session.get(url=company_url)
                soup = BeautifulSoup(
                    resp.text,
                    features='lxml')

                collected_urls = []
                found_contact = False
                for link in soup.find_all('a', href=True):
                    if 'contact' in link['href']:
                        found_contact = True
                        if 'http' in link['href']:
                            collected_urls.append(link['href'])
                        else:
                            final_url = company_url + '/' + link['href']
                            collected_urls.append(final_url)
                if not found_contact:
                    collected_urls.append(company_url)
                self.update_urls(set(collected_urls))

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
                print(f'found :: {url_guess}')
                if attempt.status_code >= 200:
                    return url_guess
            except requests.exceptions.ConnectionError:
                continue
            except requests.exceptions.ReadTimeout:
                continue
            except requests.exceptions.TooManyRedirects:
                continue

    def update_urls(self, collected_urls):
        '''
        adds urls to text file under data/scraped
        '''
        path_name = self.filepath + self.index + '/data.txt'

        with open(path_name, 'a+') as f:
            for url in collected_urls:
                f.write(f'{url}\n')
                print(f'added :: {url}')

    def create_dir(self, path_name):
        '''
        creates new directory and adds index if duplicate
        '''
        dirname = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(dirname, path_name)

        index = ''
        while True:
            try:
                os.makedirs(filepath + index)
                break
            except WindowsError:
                if index:
                    # Append 1 to number in brackets
                    index = '(' + str(int(index[1:-1]) + 1) + ')'
                else:
                    index = '(1)'
                # Go and try create file again
                pass

        return index, filepath
