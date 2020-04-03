import numpy as np
import multiprocessing as multi
import os
import re
import requests

from user_agent import generate_user_agent


def chunks(n, page_list):
    '''
    splits the list into n chunks
    used for multiprocessing
    '''
    return np.array_split(page_list, n)


class scraper:

    def start(self, urls):
        '''
        creates text file of contact emails from given urls
        '''
        self.index, self.filepath = self.create_dir(
            path_name='../data/scraped/collected_emails')

        cpus = multi.cpu_count()
        workers = []
        url_bins = chunks(cpus, urls)

        for cpu in range(cpus):
            worker = multi.Process(
                name=str(cpu),
                target=self.get_contact_email,
                args=(url_bins[cpu],))

            worker.start()
            workers.append(worker)

    def get_contact_email(self, urls, test):
        '''
        uses simple crawler to extract
        email addresses from web page
        '''
        session = requests.Session()
        session.headers.update({'User-Agent': generate_user_agent(
            device_type='desktop',
            os=('mac', 'linux'))})

        for url in urls:
            # gather page content from url
            try:
                print(f'crawling :: {url}')
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
                r'(?!\S*\.(?:jpg|png|gif|bmp)(?:[\s\n\r]|$|"))[A-Z0-9._%+-]'
                '+@[A-Z0-9.-]{3,65}\.[A-Z]{2,4}',
                page_content.text,
                re.I))

            # remove duplicate emails when in lowercase
            new_emails = set([email.lower() for email in new_emails])
            print(f'new emails :: found {len(new_emails)}')

            # if not being ran in unittest
            if not test:
                self.add_collected_emails(new_emails)
            else:
                return new_emails

    def add_collected_emails(self, emails):
        '''
        adds emails to text file under data/scraped
        '''
        path_name = self.filepath + self.index + '/data.txt'

        with open(path_name, 'a+') as f:
            for email in emails:
                f.write(f'{email}\n')
            print(f'[updated]{len(emails)} emails added')

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
