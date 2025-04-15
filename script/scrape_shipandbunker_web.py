# https://shipandbunker.com/prices/apac/sea/sg-sin-singapore#IFO380

from datetime import datetime
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from script.config import IFO380_dict, MGO_dict, MEOHVLSF_dict, MEOHMGOe_dict, LSMGO_dict, MEOH_dict


def _convert_date(date_str):
    if date_str == "Feb 29":
        return "2024-02-29"
    current_year = datetime.today().year
    date_obj = datetime.strptime(date_str, '%b %d').replace(year=current_year)
    # Convert the date object to the string with the format "MM-DD"
    return date_obj.strftime('%Y-%m-%d')


def _filter_data(data_dict: dict):
    today = datetime.today()
    all_key_dates = []
    for key_date in data_dict.keys():
        all_key_dates.append(key_date)
    bad_key_dates = [key_date for key_date in all_key_dates if datetime.strptime(key_date, '%Y-%m-%d') > today]
    for bkd in bad_key_dates:
        data_dict.pop(bkd)
    return data_dict


def get_data(name='IFO_380',
             url='https://shipandbunker.com/prices/apac/sea/sg-sin-singapore#IFO380',
             class_name='price-table IFO380',
             caption='IFO380 in Singapore',
             headers='price-IFO380'):
    try:
        print(f"start scraping {name} website....")
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

        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located(
        #         (By.CLASS_NAME, f'{class_name}')))

        driver.implicitly_wait(10)

        print("opened browser...")

        xpath_expression = f"//table[contains(@class, '{class_name}') and contains(@caption, '{caption}')]"
        table_element = driver.find_element(By.XPATH, xpath_expression)

        # Get the HTML content of the table
        table_html = table_element.get_attribute('outerHTML')

        soup = BeautifulSoup(table_html, 'html.parser')

        # Find the table by class name
        table = soup.find('table', class_=f'{class_name}')

        # Initialize an empty dictionary to store the data
        ifo_data = {}

        # Iterate over each row in the table body
        for row in table.find_all('tr'):
            # Find the date cell and the price cell
            date_cell = row.find('th', class_='date')
            price_cell = row.find('td', headers=f'{headers}')

            # Check if the cells exist and extract text
            if date_cell and price_cell:
                date = date_cell.get_text(strip=True)
                price = price_cell.get_text(strip=True)

                # Remove any unwanted characters or whitespace
                date = date[1:]
                print(date)
                # date = date.replace('F', '').replace('T', '').replace('W', '').replace('M', '').strip()
                # date = (date.split(' ')[1] + ' ' + date.split(' ')[2]).strip()
                price = price.split()[0]  # Assuming the price is the first number before any whitespace

                # Add the data to the dictionary
                ifo_data[_convert_date(date)] = price

        print(ifo_data)

        # Don't forget to close the browser
        driver.quit()

        filtered_data = _filter_data(ifo_data)
        print(f"end scraping {name} website....")
        return filtered_data

    except (URLError, HTTPError) as e:
        print(e)
        return None


def get_data_from_config_dict(config_dict):
    print(config_dict)
    return get_data(
        name=config_dict['name'],
        url=config_dict['url'],
        class_name=config_dict['class_name'],
        caption=config_dict['caption'],
        headers=config_dict['headers']
    )


if __name__ == '__main__':
    all_configs = [
        IFO380_dict,
        MGO_dict,
        MEOHVLSF_dict,
        MEOHMGOe_dict,
        LSMGO_dict,
        MEOH_dict
    ]
    print(get_data_from_config_dict(MEOH_dict))
