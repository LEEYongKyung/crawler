import ssl
from datetime import datetime
from urllib.request import Request, urlopen


def crawling(url='', encoding='utf-8'):
    try:
        request = Request(url)

        ssl._create_default_https_context = ssl._create_unverified_context
        resp = urlopen(request)

        try:
            receive = resp.read()
            result = receive.decode(encoding)
        except UnicodeDecodeError:
            result = receive.decode(encoding, 'replace')

        print('%s : success for reuqest(%s)' % (datetime.now(), url))

        return result
    except Exception as e:
        print('%s : %s' % (e, datetime.now()))