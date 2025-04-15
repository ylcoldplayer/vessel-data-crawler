# /r/cms/shibor/chinamoney/html/shiborOrg/lpr-shibor.html

import requests
from bs4 import BeautifulSoup


def get_lpr_data():
    url = 'https://www.shibor.org/r/cms/www/chinamoney/data/currency/bk-lpr.json'

    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        json_data = response.json()

        date = json_data['data']['showDateCN'].split(' ')[0]
        print(date)

        records = json_data['records']

        lpr_dict = {}
        for record in records:
            lpr_dict[record['termCode']] = record['shibor']

        data_dict = {}
        data_dict['LPR1Y'] = lpr_dict['1Y']
        data_dict['LPR5Y'] = lpr_dict['5Y']

        print(data_dict)
        return date, data_dict
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None, None


if __name__ == '__main__':
    get_lpr_data()

