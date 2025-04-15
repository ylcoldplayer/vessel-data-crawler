import requests
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re


def get_scfi_data():
    try:
        print('start scraping scfi website...')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get('https://www.sse.net.cn/index/singleIndex?indexType=scfi', headers=headers)

        bs = BeautifulSoup(response.text, 'html.parser')

        hd = bs.find('table', {'class': 'lb1'})

        rows = hd.find_all('tr')
        data = {}
        for row in rows:
            cells = row.find_all('td')
            if cells and '综合指数 Comprehensive Index' in cells[0].get_text():
                index_name = cells[0].get_text()
                last_period = cells[3].get_text()
                this_period = cells[4].get_text()
                data['name'] = '综合指数 Comprehensive Index'
                data['this_period'] = this_period
                data['last_period'] = last_period
                print(
                    f"Index Name: {index_name}, Last Period: {last_period}, This Period: {this_period}")
            elif cells and '航线' == cells[0].get_text():
                last_date = cells[3].get_text()
                this_date = cells[4].get_text()
                date_pattern = r'\d{4}-\d{2}-\d{2}'
                last_date_match = re.search(date_pattern, last_date)
                if last_date_match:
                    data['last_date'] = last_date_match.group()
                else:
                    data['last_date'] = None
                this_date_match = re.search(date_pattern, this_date)
                if this_date_match:
                    data['this_date'] = this_date_match.group()
                else:
                    data['this_date'] = None
        print('end scraping scfi website...')
        return data
    except (URLError, HTTPError) as e:
        print(e)
        return None
