from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service

if __name__ == '__main__':
    # webdriver_path = './chromedriver_mac64/chromedriver'
    service = Service(executable_path='../script/chromedriver-mac-x64/chromedriver')
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")


    # Set up driver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the page
    driver.get("https://www.balticexchange.com/en/index.html")

    # Wait for some time if needed, or perform actions like clicking the cookie accept button
    # driver.implicitly_wait(10)

    # Get page source and close the driver
    page_source = driver.page_source
    driver.quit()

    # Use BeautifulSoup or other parsing library to parse the page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    print(soup)
    # Now you can use soup to find elements, parse data, etc.
