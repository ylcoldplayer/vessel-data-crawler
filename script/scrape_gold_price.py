from urllib.error import HTTPError, URLError
from selenium.webdriver.common.by import By
import re


def get_gold_price_data():
    try:
        url = 'https://finance.sina.com.cn/futures/quotes/XAU.shtml'
        print(f"start scraping gold price website: {url}")

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
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Go to the webpage
        driver.get(url)

        bs = BeautifulSoup(driver.page_source, 'html.parser')


        print("opened browser...")

        # Wait for JavaScript to load
        driver.implicitly_wait(10)
        # print(driver.page_source)

        # find elements just like with BeautifulSoup
        # div_element = driver.find_element(By.CLASS_NAME, 'real-price price red')

        div_element = bs.find('span', {'class': re.compile(r'real-price price *')})

        # Get the text or any other attribute you need from the div element
        gold_price = div_element.text

        date_element = bs.find('p', {'class': 'trade-time time'})
        date = date_element.text.split(' ')[0]

        driver.quit()

        data['this_date'] = date

        data['this_period'] = gold_price

        print(data)

        print("end scraping gold price website....")
        return data

    except (URLError, HTTPError) as e:
        print(e)
        return None


if __name__ == '__main__':
    get_gold_price_data()
