import re

import requests
from bs4 import BeautifulSoup


def get_msci_data():
    try:
        print("start scraping msci website...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get('https://www.marketscreener.com/quote/index/MSCI-WORLD-TRANSPORTATION-121735109/graphics/',
                                headers=headers)
        bs = BeautifulSoup(response.text, 'html.parser')

        html_content = bs.find('div', {'class': 'c-12 cm-auto border-right'})

        for td in html_content.find_all('td'):
            if td.find('sup') and 'SEK' in td.sup.get_text():
                original_string = td.sup.parent.get_text()
                cleaned_string = "\n".join(line for line in original_string.splitlines() if line.strip())
                data_text_raw = cleaned_string.splitlines()[0].strip()
                data_text = ''.join(data_text_raw.split(','))
                print(data_text)

            date_span = td.find('span', attrs={'data-field': 'datetime', 'data-format': "h:i:s Y-m-d a T"})
            if date_span is not None:
                date = date_span.get_text().split(' ')[1]
                print(date)
                break

        print("end scraping msci website...")


        match = re.search(r'\d+\.?\d*', data_text)
        if match:
            data_text = match.group()

        print("this_period: ", data_text)
        print("this_date: ", date)

        return {'this_period': data_text, 'this_date': date}
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    get_msci_data()