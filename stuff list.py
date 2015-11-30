# -*- coding: utf-8 -*-

import time
import urllib
import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
}

print "每頁商品清單"
user_input = raw_input('Search key word:')
item_link = "k={}&t=0".format(
    urllib.quote(user_input))  # add link
page_link = item_link + '&p={}'
results = []
sleep = time.sleep(2)


def lazy(page_link):

    page_link = page_link.format(1)  # get total-page and total-items first
    # print page_link

    target = requests.get(page_link, headers=headers)
    target.encoding = ''  # add encode
    soup = BeautifulSoup(target.text)

    total_page = soup.select('.total-page')
    total_items = soup.select('.total')
    print "Total items: " + total_items[0].text
    print "Total pages: " + total_page[0].text

    end_page = int(raw_input('Enter the end page range:'))
    page_range = range(0, end_page)
    page = 0

    for num in page_range:
        page += 1
        search_link = page_link.format(num)

        res = requests.get(search_link, headers=headers)
        res.encoding = ""  # add encode
        soup = BeautifulSoup(res.text)

        title = soup.select('.entry-title')
        price = soup.select('.price')
        totaltimes = soup.select('.total-times')
        seller = soup.select('.id')
        feedback = soup.select('.estimate')

        for num in range(0, 30):  # one page has 30 items
            results.append(str(page) + ',' + title[num].text + ',' + price[num].text + ',' + totaltimes[num].text + ',' +
                           seller[num].text + ',' + feedback[num].text.rstrip(')'))

        # print results
        print "頁數,商品名稱,商品價格,出價次數,賣家帳號,賣家評價"
        for data in results:
            print data

        sleep

lazy(page_link)
