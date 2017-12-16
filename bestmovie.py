from multiprocessing import Pool, Manager
import multiprocessing
import requests
from bs4 import BeautifulSoup
import time
import re

def useweb1(code):
    '''
    使用https://idope.se/torrent-list/获取对于番号的磁力链
    :param code:
    :return:
    '''
    url_root1 = 'https://idope.se'
    search_url1 = 'https://idope.se/torrent-list/'
    headers ={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    r1 = requests.get(search_url1+code,headers=headers)
    content1 = r1.text
    soup1 = BeautifulSoup(content1, 'html.parser')
    url_1 = soup1.find('a',href=re.compile(code))['href']
    r2 = requests.get(url_root1+url_1)
    content2 = r2.text
    soup2 = BeautifulSoup(content2, 'html.parser')
    magnet = soup2.find('div', id='deteails')
    if magnet:
        return(magnet.text)
    return ''


def useweb2(code):
    '''
    使用https://btso.pw/search/来查找番号
    :param code:
    :return:
    '''
    search_url2 = 'https://btso.pw/search/'
    headers ={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    proxies = {
      'http' : '127.0.0.1:1087',
      'https': '127.0.0.1:1087'
    }
    r1 = requests.get(search_url2+code,headers=headers,proxies=proxies)
    content1  = r1.text
    soup1 = BeautifulSoup(content1, 'html.parser')
    url_1 = soup1.find('a', href=re.compile('/detail/hash/'))['href']
    r2 = requests.get(url_1, headers=headers, proxies=proxies)
    content2 = r2.text
    soup2 = BeautifulSoup(content2, 'html.parser')
    magnet = soup2.find('textarea','magnet-link')
    if magnet:
        return magnet.text
    return ''

def DealCookies(cookie):
    cookies = {}
    for line in cookie.split(';'):  # 按照字符：进行划分读取
        # 其设置为1就会把字符串拆分成2份
        name, value = line.strip().split('=', 1)
        cookies[name] = value  # 为字典cookies添加内容
    return cookies


def GUrl(starturl):
    '''
    生成URL
    '''
    urls = []
    urls.append(starturl)
    for i in range(2,26):
        u = 'http://www.javlibrary.com/cn/vl_bestrated.php?&mode=&page='+str(i)
        urls.append(u)
    return urls

def GetAVcode():
    '''
    从URL中获得每一页的AV code
    '''
    codelist = []
    starturl = 'http://www.javlibrary.com/cn/vl_bestrated.php'
    urls = GUrl(starturl)
    for url in urls:
        proxies = {
            'http': '127.0.0.1:1087',
            'https': '127.0.0.1:1087'
        }
        cookie = '__cfduid=d6584d181c0072c52af034f471e4910441513402641; timezone=-480; __utma=45030847.784005738.1513402642.1513402642.1513402642.1; __utmz=45030847.1513402642.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); sc_is_visitor_unique=rx8499656.1513402643.8C5475D9B4614FA64DC9DF6890F377AA.1.1.1.1.1.1.1.1.1; __qca=P0-1312521764-1513402642581; __utma=45030847.784005738.1513402642.1513402642.1513402642.1; __utmz=45030847.1513402642.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __atuvc=3%7C50; __atuvs=5a34e264283c7914000; over18=18'
        cookies = DealCookies(cookie)
        r = requests.get(url, proxies=proxies, cookies=cookies)
        content= r.text
        soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
        # 找class为id的div
        codes = soup.find_all('div', 'id')
        for code in codes:
            codelist.append(code.text)
            print('Get====='+code.text)
    return codelist

def write(code,con):
    file_path = './study_movie.txt'
    f = open(file_path, 'a+')
    f.write(code+'\n'+con+'\n\n')
    f.close()


def GetAVmagnet(code):
    '''
    通过AV code从磁力搜索引擎上获得磁力链，其中一个获得不到结果，就使用第二个
    '''
    magnet = useweb1(code)
    if magnet:
        write(code, magnet)
    else:
        magnet = useweb2(code)
        write(code, magnet)
    print(code + '=====over')


if __name__ == '__main__':
    codelist = GetAVcode()
    cpus = multiprocessing.cpu_count()
    p = Pool(cpus)
    for code in codelist:
        p.apply_async(GetAVmagnet, args=(code,))
    p.close()
    p.join()

