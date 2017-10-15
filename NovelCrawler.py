# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 19:13:21 2017

@author: raceh
"""
import os
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def getHTMLText(url):
    try:
        kv = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url, headers = kv, timeout = 30)
        r.raise_for_status() #如果状态不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '产生异常'

def get_feilun():
    f = open('d:\\费伦蝶影.txt', 'w', encoding = 'utf-8')

    for i in range(2, 233): #233
        url = 'http://www.hftcjy.com/qhuan/199117/' + str(i) + '.html'
        html = getHTMLText(url)
        soup = BeautifulSoup(html, 'html.parser')

        #读入章节标题
        meta = soup.find('meta', attrs = {'name':'keywords'})
        if meta:
            title = meta.attrs['content']
            f.write(title)
            f.write(u'\r\n')

        #读入章节内容
        div = soup.find('div', attrs = {'class':'text bookreadercontent'})
        if div:
            paragraphs = div.find_all('p')
            for p in paragraphs:
                f.write(p.text.strip())
                f.write(u'\r\n')

        f.write(u'\r\n')
        print('chapter {0} done!'.format(i))

    f.close()

def get_hbooker(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')

    #读入书名
    book_name = ''
    break_crumb_tag = soup.find('div', attrs = {'breakcrumb ly-fl'})
    a_tags = break_crumb_tag.find_all('a')
    for a_tag in a_tags:
        if a_tag['href'] == 'http://hbooker.com/index': #首页
            continue
        book_name = a_tag.text

    if not book_name: #没有读到内容
        return

    #读入章节url
    chapter_url_list = []
    mod_box_tags = soup.find_all('div', attrs = {'class':'book-chapter-list'})
    for mod_box_tag in mod_box_tags:
        a_tags = mod_box_tag.find_all('a')
        for a_tag in a_tags:
            chapter_url_list.append(a_tag['href'])

    f = open('d:\\' + book_name + '.txt', 'w')
    driver = webdriver.Chrome()

    if not chapter_url_list: #没有读到内容
        return

    #从每个章节页面抓取内容
    for chapter_url in chapter_url_list:
        try:
            driver.get(chapter_url)
            #切换iframe
            driver.switch_to.frame('chapter')  #用id来定位
            #driver.switch_to.frame(1)  #用frame的index来定位，第一个是0
            #driver.switch_to.frame('chapter')  #用name来定位
            #driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))  #用WebElement对象来定位
            
            data = driver.page_source #取到加载js后的页面内容
            soup = BeautifulSoup(data, 'html.parser')
            h3_tag = soup.find('h3', attrs = {'class':'chapter'})
            title = h3_tag.contents[0]
            f.write(title)
            f.write('\r\n')
            p_tags = soup.find_all('p', attrs = {'class':'chapter'})
            
            for p_tag in p_tags:
                p = p_tag.contents[0]
                f.write(p)
                f.write('\r\n')
    
            f.write('\r\n')
        except:
            continue

    driver.quit()
    f.close()

if __name__ == '__main__':
    #get_feilun()
    get_hbooker('http://hbooker.com/chapter-list/100017879/book_detail')
