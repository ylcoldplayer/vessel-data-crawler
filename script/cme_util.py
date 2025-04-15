import datetime
import io
import json
import os
import sys
import time
from time import sleep
import requests
from bs4 import BeautifulSoup
import lxml
from urllib.parse import urlencode


# now_time = int(time.time() * 1000)
# TODAY = datetime.date.today()
# TODAY_str = str(TODAY)
# JSON_FILE_PATH = os.path.join(os.path.dirname(sys.argv[0]), 'cmegroup-{}-{}.json'.format(TODAY_str, now_time))

def get_cme_data():
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
    }

    url = 'https://www.cmegroup.com/services/sofr-strip-rates/?isProtected&_t=1701315778000'

    response = requests.get(url=url, headers=headers)
    print(response.text)
    content_json = response.json()

    prd_list = content_json['resultsStrip']
    prd_result_list = []
    for prd_item in prd_list:
        prd_dict = {'date': prd_item['date'], 'sofr': {
            'overnight': prd_item['overnight'],
            'index': prd_item['index']
        }, 'sofr averages': {
            '30-day avg': prd_item['average30day'],
            '90-day avg': prd_item['average90day'],
            '180-day avg': prd_item['average180day']
        }, 'cme term sofr': {}}
        prd_cme_list = prd_item['rates']['sofrRatesFixing']
        for prd_cme_list_item in prd_cme_list:
            prd_dict['cme term sofr'].update(
                {
                    prd_cme_list_item['term']: prd_cme_list_item['price']
                }
            )
        # print(prd_dict)
        prd_result_list.append(prd_dict)
        break
    return prd_cme_list

# # print(prd_result_list)
# with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f_first:
#     json.dump({'cmegroup': prd_result_list}, f_first, ensure_ascii=False, indent=2)
#
# print('{} 爬取完成...'.format(TODAY_str))


if __name__ == '__main__':
    get_cme_data()
