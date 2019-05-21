from bs4 import BeautifulSoup

html = '<td class="title balck bold"><div class="tit3" id="div-title">' \
       '<a href="/movie/bi/mi/basic.nhn?code=174065" title="걸캅스">걸캅스</a></div></td>'

#1. 조회
def ex1():
    bs = BeautifulSoup(html, 'html.parser')
    print(bs)

    tag = bs.a
    print(tag, type(tag))
    print(tag.name)


#2. 속성(attributes) 가져오기
def ex2():
    bs = BeautifulSoup(html, 'html.parser')

    tag = bs.td
    print(tag['class'])

    tag = bs.div
    print(tag['id'])
    print(tag.attrs)


#3. Attribute 조회
def ex3():
    bs = BeautifulSoup(html, 'html.parser')

    tag = bs.find('td', attrs={'class': 'title'})
    print(tag)

    tag = bs.find(attrs={'title': '걸캅스'})
    print(tag)

    tag = bs.find('td')
    print(tag)

if __name__ == '__main__':
#    ex1()
#    ex2()
    ex3()
