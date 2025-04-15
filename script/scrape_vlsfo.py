from datetime import datetime
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def _convert_date(date_str):
    if date_str == "Feb 29":
        return "2024-02-29"
    current_year = datetime.today().year
    print(date_str)
    date_obj = datetime.strptime(date_str, '%b %d').replace(year=current_year)
    # Convert the date object to the string with the format "MM-DD"
    print(date_obj.strftime('%Y-%m-%d'))
    return date_obj.strftime('%Y-%m-%d')


def get_vlsfo_data():
    try:
        print("start scraping vlsfo website....")

        service = Service(executable_path='../script/chromedriver-mac-x64/chromedriver')
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Set up driver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Go to the webpage
        driver.get('https://shipandbunker.com/prices/apac/sea/sg-sin-singapore#VLSFO')

        print("opened browser...")

        xpath_expression = "//table[contains(@class, 'price-table VLSFO') and contains(@caption, 'VLSFO in Singapore')]"
        table_element = driver.find_element(By.XPATH, xpath_expression)

        # Get the HTML content of the table
        table_html = table_element.get_attribute('outerHTML')

        soup = BeautifulSoup(table_html, 'html.parser')

        # Find the table by class name
        table = soup.find('table', class_='price-table VLSFO')

        # Initialize an empty dictionary to store the data
        vlsfo_data = {}

        # Iterate over each row in the table body
        for row in table.find_all('tr'):
            # Find the date cell and the price cell
            date_cell = row.find('th', class_='date')
            price_cell = row.find('td', headers='price-VLSFO')

            # Check if the cells exist and extract text
            if date_cell and price_cell:
                date = date_cell.get_text(strip=True)
                price = price_cell.get_text(strip=True)

                # Remove any unwanted characters or whitespace
                date = date[1:]
                price = price.split()[0]  # Assuming the price is the first number before any whitespace

                # Add the data to the dictionary
                vlsfo_data[_convert_date(date)] = price

        print(vlsfo_data)

        # Don't forget to close the browser
        driver.quit()


        print("end scraping vlsfo website....")
        return vlsfo_data

    except (URLError, HTTPError) as e:
        print(e)
        return None


if __name__ == '__main__':
    get_vlsfo_data()
