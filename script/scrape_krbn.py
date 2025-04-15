from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime


def trim_date(date_str):
    date_str_clean = date_str.replace('月', '')

    dt = datetime.strptime(date_str_clean, "%m %d, %Y")

    formatted_date = dt.strftime("%Y-%m-%d")
    return formatted_date

def get_krbn_data():
    try:
        print('start scraping krbn website...')
        service = Service(executable_path='../script/chromedriver-mac-x64/chromedriver')
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Set up driver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Go to the webpage
        driver.get('https://cn.investing.com/etfs/krbn-historical-data')

        driver.implicitly_wait(5)

        print(driver.page_source)

        bs = BeautifulSoup(driver.page_source, 'html.parser')
        html_content = bs.find('div', {'class': 'mt-6 flex flex-col items-start overflow-x-auto p-0 md:pl-1'})

#mt-6 flex flex-col items-start overflow-x-auto p-0 md:pl-1
        tbody = html_content.find('table').find('tbody')

        data_dict = {}

        for tr in tbody.find_all('tr'):
            tds = tr.find_all('td')
            date = tds[0].get_text()
            date = trim_date(date)
            price = tds[1].get_text()
            data_dict[date] = price
            print(date)
            print(price)

        driver.quit()
        print("end scraping krbn website...")

        print(data_dict)
        return data_dict

    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    get_krbn_data()