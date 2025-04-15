import requests
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re


def get_cdi_data():
    try:
        print("start scraping cdi website....")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get('https://www.sse.net.cn/index/singleIndex?indexType=cdi', headers=headers)

        bs = BeautifulSoup(response.text, 'html.parser')

        data = {}

        date_text = bs.find('div', {'class': 'title2'}).h5.get_text()
        date_pattern = r'\d{4}-\d{2}-\d{2}'
        date_match = re.search(date_pattern, date_text)
        if date_match:
            data['this_date'] = date_match.group()
        else:
            data['this_date'] = None

        hd = bs.find('table', {'class': 'lb1'})
        rows = hd.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            if cells and '综合指数' in cells[0].get_text():
                index_name = cells[0].get_text()
                this_period = cells[3].get_text()
                data['name'] = 'cdi综合指数'
                data['this_period'] = this_period
                print(
                    f"Index Name: {index_name}, This Period: {this_period}")
        print(data)
        print("end scraping cdi website....")

        return data
    except (URLError, HTTPError) as e:
        print(e)
        return None


if __name__ == '__main__':
    get_cdi_data()