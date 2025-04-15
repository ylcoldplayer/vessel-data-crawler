import requests
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re


def get_ctfi_data():
    try:
        url = 'https://www.sse.net.cn/index/singleIndex?indexType=ctfi'
        print(f'start scraping ctfi data from {url}')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)

        bs = BeautifulSoup(response.text, 'html.parser')
        data = {}

        date_text = bs.find('div', {'class': 'title2'}).get_text()
        date_pattern = r'\d{4}-\d{2}-\d{2}'
        last_date_match = re.search(date_pattern, date_text)
        if last_date_match:
            data['last_date'] = last_date_match.group()
        else:
            data['last_date'] = None

        hd = bs.find('table', {'class': 'lb1'})

        rows = hd.find_all('tr')
        print(rows)
        data['CTFI'] = rows[1].find_all('td')[5].get_text()

        data['CTFI_CT1_270k_index'] = rows[2].find_all('td')[5].get_text()
        data['CTFI_CT1_270k_WS'] = rows[3].find_all('td')[2].get_text()
        data['CTFI_CT1_270k_pt'] = rows[4].find_all('td')[2].get_text()
        data['CTFI_CT1_270k_TC_ss'] = rows[5].find_all('td')[2].get_text()
        data['CTFI_CT1_270k_TC_es'] = rows[6].find_all('td')[2].get_text()

        data['CTFI_CT2_260k_index'] = rows[7].find_all('td')[5].get_text()
        data['CTFI_CT2_260k_WS'] = rows[8].find_all('td')[2].get_text()
        data['CTFI_CT2_260k_pt'] = rows[9].find_all('td')[2].get_text()
        data['CTFI_CT2_260k_TC_ss'] = rows[10].find_all('td')[2].get_text()
        data['CTFI_CT2_260k_TC_es'] = rows[11].find_all('td')[2].get_text()



        # for row in rows:
        #     cells = row.find_all('td')
        #     if cells and '中国出口集装箱运价综合指数' in cells[0].get_text():
        #         index_name = cells[0].get_text()
        #         last_period = cells[1].get_text()
        #         this_period = cells[2].get_text()
        #         change = cells[3].get_text()
        #         data['name'] = '中国出口集装箱运价综合指数'
        #         data['this_period'] = this_period
        #         data['last_period'] = last_period
        #         print(
        #             f"Index Name: {index_name}, Last Period: {last_period}, This Period: {this_period}, Change: {change}")
        #     elif cells and '航线' == cells[0].get_text():
        #         last_date = cells[1].get_text()
        #         this_date = cells[2].get_text()
        #         date_pattern = r'\d{4}-\d{2}-\d{2}'
        #         last_date_match = re.search(date_pattern, last_date)
        #         if last_date_match:
        #             data['last_date'] = last_date_match.group()
        #         else:
        #             data['last_date'] = None
        #         this_date_match = re.search(date_pattern, this_date)
        #         if this_date_match:
        #             data['this_date'] = this_date_match.group()
        #         else:
        #             data['this_date'] = None
        print(data)
        print(f'end scraping ctfi data from {url}')
        return data
    except (URLError, HTTPError) as e:
        print(e)
        return None


if __name__ == '__main__':
    get_ctfi_data()
