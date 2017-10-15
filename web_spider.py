# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 17:48:48 2017

@author: raceh
"""

import requests
import os

from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        kv = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url, headers = kv, timeout = 30)
        r.raise_for_status() #如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '产生异常'

#说明：url中问号是分隔的作用，表明后面是请求这网页时提供的参数。格式是参数名=参数的值，多个参数用&分开。
def search(url, param, keyword):
    try:
        kv = {param:keyword}
        r = requests.get(url, params = kv, timeout = 30)
        print(r.request.url)
        r.raise_for_status() #如果状态不是200，引发HTTPError异常
        print(len(r.text))
        return r.text
    except:
        return '产生异常'

def getFile(url, path):
    path += url.split('/')[-1]
    if os.path.exists(path):
        print('文件已存在')
    else:
        try:
            r = requests.get(url)
            r.raise_for_status() #如果状态不是200，引发HTTPError异常
            with open(path, 'wb') as f:
                f.write(r.content)
                print('文件保存成功')
        except:
            print('产生异常')

if __name__ == '__main__':
    url = 'https://www.amazon.cn/dp/B06WWBG3JJ/ref=gwgfloorv1_CE_bal_1?pf_rd_p=05b45cee-1b6d-43b4-ba8a-d2ac26fc8576&pf_rd_s=desktop-7&pf_rd_t=36701&pf_rd_i=desktop&pf_rd_m=A1AJ19PSB66TGU&pf_rd_r=QPR3Y7XFXWYE4GT1Q4MX&pf_rd_r=QPR3Y7XFXWYE4GT1Q4MX&pf_rd_p=05b45cee-1b6d-43b4-ba8a-d2ac26fc8576'
    print(getHTMLText(url)[:1000])

    search('http://www.baidu.com/s', 'wd', 'Python')
    search('http://www.so.com/s', 'q', 'Python')
    search('http://cn.bing.com/search', 'q', 'Python')

    getFile('http://i0.hexunimg.cn/2013-02-19/151233181.jpg', 'D:/')
    print(search('http://m.ip138.com/ip.asp', 'ip', '59.172.181.156')[-500:])
