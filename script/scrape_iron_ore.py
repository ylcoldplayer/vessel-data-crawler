# class = 'page-title symbol-header-info   ng-scope'
# url = 'https://www.barchart.com/futures/quotes/TR*0/futures-prices'
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re


def _convert_date(date_str):
    clean_date_str = re.sub(r'(st|nd|rd|th),', ',', date_str)
    date_obj = datetime.strptime(clean_date_str, '%a, %b %d, %Y')
    formatted_date = date_obj.strftime('%Y-%m-%d')

    return formatted_date


def get_iron_ore_data():
    try:
        print("start scraping iron ore website...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get('https://www.barchart.com/futures/quotes/TR*0/futures-prices', headers=headers)

        # print(response.text)
        div_content = \
            BeautifulSoup(response.text, 'html.parser').find('div', {'class': 'page-title symbol-header-info'})[
                'data-ng-init']

        # Regular expressions to extract the specific data
        last_price_pattern = re.compile(r'"lastPrice":"(.*?)s"')
        session_date_pattern = re.compile(r'"sessionDateDisplayLong":"(.*?)"')

        # Search for patterns
        last_price_match = last_price_pattern.search(div_content)
        session_date_match = session_date_pattern.search(div_content)

        # Extract the matched data
        last_price = last_price_match.group(1) if last_price_match else None
        session_date = session_date_match.group(1) if session_date_match else None
        this_date = _convert_date(session_date)

        data = {}
        data['this_period'] = last_price
        data['this_date'] = this_date
        print(data)
        print("start scraping iron ore website...")

        return data
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    get_iron_ore_data()
