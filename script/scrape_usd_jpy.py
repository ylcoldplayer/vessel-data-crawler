from datetime import datetime
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from mechanize import Browser



def get_usd_jpy_data():
    try:
        url = 'https://cn.investing.com/currencies/usd-jpy'
        print(f"start scraping usd_jpy website: {url}")

        b = Browser()
        b.set_handle_robots(False)
        b.addheaders = [('Referer', url), ('User-agent',
                                                                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        b.open(url)
        bs = BeautifulSoup(b.response().read(), "html.parser")

        # print(bs)

        usd_jpy_data = bs.find('div', {'class': 'text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]'})
        data = {}
        data['this_period'] = usd_jpy_data.get_text()
        today = datetime.today().strftime('%Y-%m-%d')
        data['this_date'] = today


        print(data)

        print(f"end scraping usd_cny website: {url}")
        return data

    except (URLError, HTTPError) as e:
        print(e)
        return None


if __name__ == '__main__':
    get_usd_jpy_data()