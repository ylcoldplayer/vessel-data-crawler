# url = 'https://www.epanasia.com/freightIndex/'
from datetime import datetime
from urllib.error import URLError, HTTPError

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


def get_xhpdci_data():
    try:
        url = 'https://www.epanasia.com/freightIndex/'
        print(f"start scraping xh pdci website: {url}")

        data = {}

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        service = Service(executable_path='../script/chromedriver-mac-x64/chromedriver')
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Set up driver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navigate to the website
        driver.get(url)
        # driver.implicitly_wait(10)

        def wait_for_number_change(driver):
            element = driver.find_element(By.ID, 'freight-index')
            text = element.text
            return text != '0'
            # return text != '0' and text.isdigit()

        # Wait for a specific element to be loaded
        WebDriverWait(driver, 30).until(wait_for_number_change)


        print(driver.page_source)


        # # Now get the HTML content
        # nhci_data = driver.find_element(By.CLASS_NAME, 'contract-detail-price').text
        #
        # # Close the browser
        # driver.quit()
        #
        # data['this_period'] = nhci_data
        # today = datetime.today().strftime('%Y-%m-%d')
        # data['this_date'] = today
        #
        # print(data)
        # print("end scraping 南华 website....")
        # return data

    except (URLError, HTTPError) as e:
        print(e)
        return None, None


if __name__ == '__main__':
    get_xhpdci_data()
