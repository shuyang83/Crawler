# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 10:36:00 2017

@author: raceh
"""

import requests
import bs4
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        r = requests.get(url, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('产生异常')
        return ''

def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.find('tbody').children: #children是子节点的迭代类型
        if isinstance(tr, bs4.element.Tag):
            td_index = tr.find('td') #只返回一个td
            tds = td_index('td') #等价于td_index.find_all('td')，返回结果是一个列表
            ulist.append([td_index.contents[0], tds[0].string, tds[2].string])

def printUnivList(ulist, num):
    tplt = '{0:^10}\t{1:{3}^10}\t{2:^10}'
    print(tplt.format('排名', '学校名称', '总分', chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0], u[1], u[2], chr(12288)))

def main():
    uinfo = []
    url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2017.html'
    html = getHTMLText(url)
    if html != '':
        fillUnivList(uinfo, html)
        printUnivList(uinfo, 20) #打印前20所大学

main()