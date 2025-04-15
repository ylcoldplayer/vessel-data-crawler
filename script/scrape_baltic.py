# url = 'https://www.balticexchange.com/en/index.html'

from datetime import datetime
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from util import percent_to_decimal


def convert_date_format(date_string):
    date_obj = datetime.strptime(date_string, '%d %b %Y')
    new_date_format = date_obj.strftime('%Y-%m-%d')
    return new_date_format


def get_baltic_data():
    url = 'https://seecapitalmarkets.com/ShippingIndexes'

    try:
        print("start scraping baltic website....")

        service = Service(executable_path='../script/chromedriver-mac-x64/chromedriver')
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Set up driver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Go to the webpage
        driver.get(url)

        # WebDriverWait(driver, 60).until(
        #     EC.visibility_of_element_located(
        #         (By.ID, 'ticker')))

        # WebDriverWait(driver, 60).until(
        #     EC.title_is('Indices')
        # )

        print("opened browser...")
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        print(soup)

        # rates_table = soup.find(
        #     lambda tag: tag.name == 'h2' and '1-month Term SOFR swap rate' in tag.text).parent.parent
        #
        # rates_dict = {}
        #
        # rows = rates_table.find_all('tr')
        #
        # headers = rows.pop(0)
        # dates = [header.get_text(strip=True) for header in headers.find_all('th')[1:]]
        #
        # for row in rows:
        #     cells = row.find_all('td')
        #     term = cells.pop(0).get_text(strip=True)
        #
        #     term_rates = []
        #
        #     for cell, date in zip(cells, dates):
        #         rate = cell.get_text(strip=True)
        #         term_rates.append((convert_date_format(date), percent_to_decimal(rate)))
        #
        #     rates_dict[term] = term_rates
        #
        # for term, rates in rates_dict.items():
        #     print(f"{term} rates:")
        #     for date, rate in rates:
        #         print(f"  {date}: {rate}")
        #

        driver.quit()
        print("end scraping baltic website....")

        return None
    except (URLError, HTTPError) as e:
        print(e)
        return None


if __name__ == '__main__':
    get_baltic_data()


