from urllib.error import HTTPError, URLError
from selenium.webdriver.common.by import By
import re

def get_crb_data():
    try:
        print("start scraping crb website....")
        data = {}

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from bs4 import BeautifulSoup
        from selenium.webdriver.chrome.service import Service

        service = Service(executable_path='../script/chromedriver-mac-x64/chromedriver')
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Set up driver
        # from webdriver_manager.chrome import ChromeDriverManager
        # driver = webdriver.Chrome(service=ChromeDriverManager().install(), options=chrome_options)

        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Go to the webpage
        driver.get('https://quote.eastmoney.com/gb/zsCRB.html')

        print("opened browser...")

        # Wait for JavaScript to load
        driver.implicitly_wait(10)  # Adjust time according to your needs

        # Now you can find elements just like with BeautifulSoup
        div_element = driver.find_element(By.CLASS_NAME, 'zxj')

        # Get the text or any other attribute you need from the div element
        crb_value = div_element.text

        date_element = driver.find_element(By.CLASS_NAME, 'quote_title_time')
        date = date_element.text.split(' ')[0]

        driver.quit()

        date_pattern = r'\d{4}-\d{2}-\d{2}'
        this_date_match = re.search(date_pattern, date)

        if this_date_match:
            data['this_date'] = this_date_match.group()
        else:
            data['this_date'] = None

        data['this_period'] = crb_value

        print(data)

        print("end scraping crb website....")
        return data

    except (URLError, HTTPError) as e:
        print(e)
        return None


if __name__ == '__main__':
    get_crb_data()
