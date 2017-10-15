# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 19:31:00 2017

@author: raceh
"""

import requests
from bs4 import BeautifulSoup
import traceback
import re

def getHTMLText(url):
    try:
        kv = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url, headers = kv, timeout = 30)
        r.raise_for_status() #如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '产生异常'

def getStockList(lst, stock_url):
    html = getHTMLText(stock_url)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            lst.append(re.findall(r'[s][hz]\d{6}', href)[0])
        except:
            continue

def getStockInfo(lst, stock_url, fpath):
    for stock in lst:
        url = stock_url + stock + '.html'
        html = getHTMLText(url)
        try:
            if html == '':
                continue
            info_dict = {}
            soup = BeautifulSoup(html, 'html.parser')
            stock_info = soup.find('div', attrs = {'class':'stock-bets'})

            name = stock_info.find_all(attrs = {'class':'bets-name'})[0]
            info_dict.update({'股票名称':name.text.split()[0]})

            key_list = stock_info.find_all('dt')
            value_list = stock_info.find_all('dd')
            for i in range(len(key_list)):
                key = key_list[i].text
                val = value_list[i].text
                info_dict[key] = val

            print(info_dict)
        except:
            traceback.print_exc()
            continue

if __name__ == '__main__':
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    output_file = 'd:\\stock.txt'
    slist = []
    getStockList(slist, stock_list_url)
    getStockInfo(slist[300:310], stock_info_url, output_file)
