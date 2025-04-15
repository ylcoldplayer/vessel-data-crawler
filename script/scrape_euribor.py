from datetime import datetime
from urllib.error import URLError, HTTPError

import requests
from bs4 import BeautifulSoup

from script.util import percent_to_decimal


def get_euribor_data():
    try:
        print("start scraping euribor website...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get('https://www.euribor-rates.eu/en/', headers=headers)

        bs = BeautifulSoup(response.text, 'html.parser')

        date_text = bs.find('div', {'class': 'card-header'}).get_text()
        date = datetime.strptime(date_text.strip(), '%m/%d/%Y').strftime('%Y-%m-%d')
        print(date_text)

        data = bs.find('div', {'class': 'card-body'})
        print(data)

        data_dict = {}
        for row in data.find_all('tr'):
            all_tds = row.find_all('td')
            term = None
            for td in all_tds:
                if td.find('a', href=True):
                    term = td.get_text()
            if term is None:
                print('term not found in this td:')
                print(td)
                continue
            rate = row.find('td', {'class': 'text-right'}).get_text()
            data_dict[term] = percent_to_decimal(rate)

        print(data_dict)

        print("end scraping euribor website...")
        return date, data_dict

    except (URLError, HTTPError) as e:
        print(e)
        return None, None


if __name__ == '__main__':
    get_euribor_data()