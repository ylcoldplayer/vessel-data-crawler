from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()


def getLinks(pageUrl):
    global pages
    if len(pages) >= 1000:
        return
    try:
        html = urlopen('http://en.wikipedia.org{}'.format(pageUrl))
    except Exception as e:
        print(e)
        return
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)


if __name__ == '__main__':
    getLinks('')
