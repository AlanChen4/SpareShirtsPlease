import os
import re
import requests

from user_agent import generate_user_agent


class scraper:

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


if __name__ == '__main__':
    e_s = scraper()
    e_s.get_contact_email(['https://www.Springboard.com//contact/'])
