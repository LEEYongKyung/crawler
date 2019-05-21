import time
from datetime import datetime
from bs4 import BeautifulSoup
from itertools import count
from pandas import DataFrame
from selenium import webdriver
from crawler import crawling


def crawling_nene():
    results = []
    first_shopname_prevpage = ''

    for page in count(start=1):
        html = crawling('https://nenechicken.com/17_new/sub_shop01.asp?ex_select=1&ex_select2=&IndexSword=&GUBUN=A&page=%d' % page)
        bs = BeautifulSoup(html, 'html.parser')

        tags_div = bs.findAll('div', attrs={'class': 'shopInfo'})

        # 끝페이지 검출
        shopname = tags_div[0].find('div', attrs={'class': 'shopName'}).text
        if first_shopname_prevpage == shopname:
            break

        first_shopname_prevpage = shopname

        for tag_div in tags_div:
            name = tag_div.find('div', attrs={'class': 'shopName'}).text
            address = tag_div.find('div', attrs={'class': 'shopAdd'}).text
            sidogu = address.split()[:2]
            results.append((name,) + tuple(sidogu))

    # store
    table = DataFrame(results, columns=['name', 'sido', 'gugun'])
    table.to_csv('results/nenne.csv', encoding='utf-8', mode='w', index=True)


def crawling_pelicana():
    results = []

    for page in count(1,):

        html = crawling('https://pelicana.co.kr/store/stroe_search.html?branch_name=&gu=&si=&page=%d' % page)
        bs = BeautifulSoup(html, 'html.parser')

        tag_table = bs.find('table', attrs={'class': 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        # 끝페이지 검출
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            sidogu = strings[3].split()[:2]
            results.append((name, ) + tuple(sidogu))

    # store
    table = DataFrame(results, columns=['name', 'sido', 'gugun'])
    table.to_csv('results/pelicana.csv', encoding='utf-8', mode='w', index=True)


def crawling_kyochon():
    results = []

    for sido1 in range(1, 18):
        for sido2 in count(start=1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' % (sido1, sido2)
            html = crawling(url)
            if html is None:
                break

            bs = BeautifulSoup(html, 'html.parser')
            tag_ul = bs.find('ul', attrs={'class': 'list'})
            tags_a = tag_ul.findAll('a')
            for tag_a in tags_a:
                tag_strong = tag_a.find('strong')
                if tag_strong is None:
                    break

                name = tag_strong.text
                strings = list(tag_a.find('em').strings)
                address = strings[0].strip('\r\n\t')
                sidogu = address.split()[:2]
                results.append((name, ) + tuple(sidogu))
    # store
    table = DataFrame(results, columns=['name', 'sido', 'gugun'])
    table.to_csv('results/kyochon.csv', encoding='utf-8', mode='w', index=True)


def crawling_goobne():
    url = 'http://www.goobne.co.kr/store/search_store.jsp'

    # 첫페이지 로딩
    wd = webdriver.Chrome('D:\PythonStudy\chromedriver\chromedriver.exe')
    wd.get(url)
    time.sleep(2)

    results = []
    for page in count(start=1):
        # 자바스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)

        print('%s : success for script execue [%s]' % (datetime.now(), script))
        time.sleep(2)

        # 실행결과(렌더링된 결과) HTML 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')

        tag_tbody = bs.find('tbody', attrs={'id': 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # 마지막 검출
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]

            results.append((name,) + tuple(sidogu))

    # store
    table = DataFrame(results, columns=['name', 'sido', 'gugun'])
    table.to_csv('results/goobne.csv', encoding='utf-8', mode='w', index=True)


if __name__ == '__main__':
    # pelicana collection
    crawling_pelicana()

    # nene collection(과제)
    crawling_nene()

    # kyochon collection
    crawling_kyochon()

    # goobne collection
    crawling_goobne()
