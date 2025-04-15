from datetime import datetime
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from util import percent_to_decimal

def convert_date_format(date_string):
    date_obj = datetime.strptime(date_string, '%d %b %Y')
    new_date_format = date_obj.strftime('%Y-%m-%d')
    return new_date_format


def get_sofr_data():
    url = 'https://www.chathamfinancial.com/technology/us-market-rates'

    try:
        print("start scraping sofr website....")

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

        print("opened browser...")

        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        # print(soup)

        rates_table = soup.find(
            lambda tag: tag.name == 'h2' and '1-month Term SOFR swap rate' in tag.text).parent.parent

        rates_dict = {}

        rows = rates_table.find_all('tr')

        headers = rows.pop(0)
        dates = [header.get_text(strip=True) for header in headers.find_all('th')[1:]]

        for row in rows:
            cells = row.find_all('td')
            term = cells.pop(0).get_text(strip=True)

            term_rates = []

            for cell, date in zip(cells, dates):
                rate = cell.get_text(strip=True)
                term_rates.append((convert_date_format(date), percent_to_decimal(rate)))

            rates_dict[term] = term_rates

        for term, rates in rates_dict.items():
            print(f"{term} rates:")
            for date, rate in rates:
                print(f"  {date}: {rate}")

        driver.quit()
        print("end scraping sofr website....")

        return rates_dict
    except (URLError, HTTPError) as e:
        print(e)
        return None


if __name__ == '__main__':
    get_sofr_data()


# 1 Year rates:
#   19 Jan 2024: 4.740%
#   22 Dec 2023: 4.681%
#   23 Jan 2023: 4.740%
# 2 Year rates:
#   19 Jan 2024: 4.166%
#   22 Dec 2023: 4.049%
#   23 Jan 2023: 4.145%
# 3 Year rates:
#   19 Jan 2024: 3.909%
#   22 Dec 2023: 3.743%
#   23 Jan 2023: 3.705%
# 5 Year rates:
#   19 Jan 2024: 3.737%
#   22 Dec 2023: 3.517%
#   23 Jan 2023: 3.341%
# 7 Year rates:
#   19 Jan 2024: 3.700%
#   22 Dec 2023: 3.462%
#   23 Jan 2023: 3.214%
# 10 Year rates:
#   19 Jan 2024: 3.703%
#   22 Dec 2023: 3.455%
#   23 Jan 2023: 3.160%
# 15 Year rates:
#   19 Jan 2024: 3.748%
#   22 Dec 2023: 3.487%
#   23 Jan 2023: 3.177%
# 30 Year rates:
#   19 Jan 2024: 3.581%
#   22 Dec 2023: 3.304%
#   23 Jan 2023: 2.966%
