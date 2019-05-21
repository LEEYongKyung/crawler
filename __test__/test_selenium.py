import time
from selenium import webdriver

wd = webdriver.Chrome('D:\PythonStudy\chromedriver\chromedriver.exe')
wd.get('http://ww.google.com')

time.sleep(5)

html = wd.page_source
print(html)

wd.quit()