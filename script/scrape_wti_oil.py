# url = 'https://www.marketwatch.com/investing/future/cl.1'


from datetime import datetime
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from util import percent_to_decimal

import re
from dateutil import parser
from selenium.webdriver.support import expected_conditions as EC


def extract_and_format_date(text):
    # Regular expression pattern to match a date in the format "MMM DD, YYYY"
    # This pattern matches any three-letter month abbreviation
    pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4}\b'

    # Search for the pattern in the text
    match = re.search(pattern, text)
    if match:
        date_str = match.group(0)
        # Parse the date string into a date object
        date_obj = parser.parse(date_str)
        # Format the date object into the desired format 'YYYY-MM-DD'
        return date_obj.strftime('%Y-%m-%d')
    else:
        return "No date found in the string"


def get_wti_oil_data():
    url = 'https://www.marketwatch.com/investing/future/cl.1'

    try:
        print(f"start scraping wti oil website: {url}")

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
        # driver.implicitly_wait(10)

        wait = WebDriverWait(driver, 30)
        element = wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'intraday__price')))


        print("opened browser...")

        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        print(soup)

        wti_price = soup.find('h2', {'class': 'intraday__price'}).find('span').get_text().strip()

        date = extract_and_format_date(soup.find('div', {'class': 'intraday__timestamp'}).get_text())

        data = {}
        data['this_period'] = wti_price
        data['this_date'] = date

        driver.quit()

        print(data)
        print("end scraping us yield website....")

        return data
    except (URLError, HTTPError) as e:
        print(e)
        return None


if __name__ == '__main__':
    get_wti_oil_data()
