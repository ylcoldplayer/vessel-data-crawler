from urllib.request import urlopen
import requests
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup

if __name__ == '__main__':
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get('https://www.sse.net.cn/index/singleIndex?indexType=ccfi', headers=headers)

        bs = BeautifulSoup(response.text, 'html.parser')

        hd = bs.find('table', {'class': 'lb1'})

        rows = hd.find_all('tr')
        data = {}
        for row in rows:
            cells = row.find_all('td')
            if cells and '中国出口集装箱运价综合指数' in cells[0].get_text():
                index_name = cells[0].get_text()
                last_period = cells[1].get_text()
                this_period = cells[2].get_text()
                change = cells[3].get_text()
                data['name'] = '中国出口集装箱运价综合指数'
                data['this_period'] = this_period
                data['last_period'] = last_period
                print(
                    f"Index Name: {index_name}, Last Period: {last_period}, This Period: {this_period}, Change: {change}")
            elif cells and '航线' in cells[0].get_text():
                last_date = cells[1].get_text()
                this_date = cells[2].get_text()
                data['last_date'] = last_date
                data['this_date'] = this_date

    except (URLError, HTTPError) as e:
        print(e)
