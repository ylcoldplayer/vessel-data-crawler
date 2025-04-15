# https://yield.chinabond.com.cn/cbweb-mn/yield_main?locale=zh_CN#
from datetime import datetime
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def get_cn_yield_data():

    url = 'https://yield.chinabond.com.cn/cbweb-cbrc-mn/cbrc/more'

    try:
        print(f"start scraping cn yield website: {url}")

        service = Service(executable_path='../script/chromedriver-mac-x64/chromedriver')
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Set up driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)

        # WebDriverWait(driver, 30).until(
        #     EC.presence_of_element_located(
        #         (By.CLASS_NAME, 'tablelist')))


        driver.get(url)

        print("opened browser...\n")

        web_content = BeautifulSoup(driver.page_source, 'html.parser')
        soup = web_content.find('div', {'id': 'gjqxData'})
        # soup = BeautifulSoup(div_content, 'html.parser')

        print(soup)
        # Find the table
        table = soup.find('table')

        # Extract date from the first header
        headers = table.find_all('th')
        date = headers[0].text.strip().split('(')[0]

        # Initialize an empty dictionary for the yield curve data
        yield_curve_data = {}

        # Find all rows in the table
        rows = table.find_all('tr')

        # Loop through rows to find the ChinaBond Government Bond Yield Curve data
        for row in rows:
            cells = row.find_all('td')
            if cells and '中债国债收益率曲线' in cells[0].text:
                # Extract the yield curve data
                durations = ['3月', '6月', '1年', '3年', '5年', '7年', '10年', '30年']
                yield_curve_data = dict(zip(durations, [float(cell.text.strip())/100.0 for cell in cells[1:]]))
                break

        driver.quit()
        # Return the date and the yield curve data

        print(yield_curve_data)
        return date, yield_curve_data

    except (URLError, HTTPError) as e:
        print(e)
        return None


if __name__ == '__main__':
    get_cn_yield_data()