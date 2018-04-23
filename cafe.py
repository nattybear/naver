from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote

from md2html.md2html import md2html

def enc(x):
    x = quote(x)
    return quote(x, encoding='cp949')

def write(access_token, clubid, menuid, subject, content):
    url = 'https://openapi.naver.com/v1/cafe/%s/menu/%s/articles'
    url = url % (clubid, menuid)
    headers = {'Authorization' : 'Bearer ' + access_token}
    subject = enc(subject)
    content = md2html(content)
    content = enc(content)
    data = 'subject=%s&content=%s' % (subject, content)
    data = data.encode('ascii')
    req = Request(url, headers=headers, data=data)
    urlopen(req)
    return 'It Works!'
