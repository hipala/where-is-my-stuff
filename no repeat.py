# -*- coding: utf-8 -*-

import time
import urllib
import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
}

print "扣除重複刊登的實際物件數"
user_input = raw_input('Search key word:')
item_link = "k={}&t=0".format(
    urllib.quote(user_input))  # add link
page_link = item_link + '&p={}'
no_repeat_items = []
sleep = time.sleep(2)


def no_repeat_item(page_link):

    page_link = page_link.format(1)
    # print page_link

    target = requests.get(page_link, headers=headers)
    target.encoding = ''  # add encode
    soup = BeautifulSoup(target.text)

    total_page = soup.select('.total-page')
    total_items = soup.select('.total')
    print "Total items: " + total_items[0].text
    print "Total pages: " + total_page[0].text

    end_page = int(raw_input('Enter the end page range: '))
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

        for num in range(0, 30):
            if title[num].text in no_repeat_items:
                pass
            else:
                no_repeat_items.append(title[num].text)

        sleep

no_repeat_item(page_link)

print "在指定的搜尋頁數內，不重複的物件數： " + str(len(no_repeat_items))
print "是否閱讀清單？"
read_list = raw_input('yes / no: ')
if read_list == "yes":
    for item in no_repeat_items:
        print item
    else:
        pass
