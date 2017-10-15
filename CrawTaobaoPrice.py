# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 22:23:24 2017

@author: raceh
"""
import requests
import re

def getHTMLText(url, **args): #args是字典形式
    try:
        r = requests.get(url, params = args, timeout = 30)
        print(r.request.url)
        r.raise_for_status() #如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '产生异常'

def parsePage(ilt, html):
    try:
        #plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        plt = re.findall(r'"view_price":"[\d.]*"', html)
        tlt = re.findall(r'"raw_title":".*?"', html) #.*是贪婪匹配，.*?是懒惰匹配
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            ilt.append([price, title])
    except:
        print('解析错误')

def printGoodsList(ilt):
    tplt = '{:4}\t{:8}\t{:16}'
    print(tplt.format('序号', '价格', '商品名称'))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))

def main():
    goods = '书包'
    depth = 2
    url = 'https://s.taobao.com/search' #url and interface name
    info_list = []
    for i in range(depth):
        try:
            html = getHTMLText(url, q = goods, s = str(i * 44))
            parsePage(info_list, html)
        except:
            continue

    printGoodsList(info_list)

main()