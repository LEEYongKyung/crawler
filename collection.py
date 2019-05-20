from bs4 import BeautifulSoup
from itertools import count
from pandas import DataFrame
from crawler import crawling


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


if __name__ == '__main__':
    # pelicana collection
    crawling_pelicana()