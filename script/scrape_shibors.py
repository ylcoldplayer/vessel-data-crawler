# url= 'https://www.shibor.org/r/cms/www/chinamoney/data/shibor/shibor.json'
import requests


def get_shibor_data():
    url = 'https://www.shibor.org/r/cms/www/chinamoney/data/shibor/shibor.json'

    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        json_data = response.json()

        date = json_data['data']['showDateCN'].split(' ')[0]
        print(date)

        records = json_data['records']

        shibor_dict = {}
        for record in records:
            shibor_dict[record['termCode']] = record['shibor']

        data_dict = {}
        data_dict['SHIBOR_ON'] = shibor_dict['O/N']
        data_dict['SHIBOR_1M'] = shibor_dict['1M']
        data_dict['SHIBOR_3M'] = shibor_dict['3M']
        data_dict['SHIBOR_6M'] = shibor_dict['6M']
        data_dict['SHIBOR_1Y'] = shibor_dict['1Y']

        print(data_dict)
        return date, data_dict
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None, None


if __name__ == '__main__':
    get_shibor_data()
