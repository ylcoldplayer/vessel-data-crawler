from datetime import datetime
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from mechanize import Browser



def get_usd_cny_data():
    try:
        print("start scraping usd_cny website....")

        b = Browser()
        b.set_handle_robots(False)
        b.addheaders = [('Referer', 'https://cn.investing.com/currencies/usd-cny'), ('User-agent',
                                                                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        b.open('https://cn.investing.com/currencies/usd-cny')
        bs = BeautifulSoup(b.response().read(), "html.parser")

        # print(bs)

        usd_index_data = bs.find('div', {'class': 'text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]'})
        data = {}
        data['this_period'] = usd_index_data.get_text()
        today = datetime.today().strftime('%Y-%m-%d')
        data['this_date'] = today


        print(data)

        print("end scraping usd_cny website....")
        return data

    except (URLError, HTTPError) as e:
        print(e)
        return None


if __name__ == '__main__':
    get_usd_cny_data()