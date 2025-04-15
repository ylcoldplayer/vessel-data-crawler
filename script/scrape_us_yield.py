# url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2024'

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


def get_us_yield_data():
    url = 'https://www.chathamfinancial.com/technology/us-market-rates'

    try:
        print(f"start scraping us yield website: {url}")

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
            lambda tag: tag.name == 'h2' and 'U.S. Treasuries' in tag.text).parent.parent

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
        print("end scraping us yield website....")

        return rates_dict
    except (URLError, HTTPError) as e:
        print(e)
        return None


if __name__ == '__main__':
    print(get_us_yield_data())
