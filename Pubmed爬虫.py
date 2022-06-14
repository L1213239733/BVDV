#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
import os
import time

def getHtmlText(url):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    try:
        html = requests.get(url, headers=headers, timeout=60)
        html.raise_for_status()
        html.encoding = r.apparent_encoding
        return html.text
    except:
        return '爬取失败！'

def parserArticleNum(html):
    soup = BeautifulSoup(html, 'html.parser')
    articleNumTag = soup.find_all('span', 'value')
    articleNum = articleNumTag[0].string
    articleNum = int(str(articleNum).replace(',', ''))
    return articleNum

def parserMainHtmlText(html):
    soup = BeautifulSoup(html, 'html.parser')
    pmidTag = soup.find_all('span', 'docsum-pmid')
    for tag in pmidTag:
        pmidLists.append(tag.string)

def parserPmidHtmlText(html, pmid):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        titleTag = soup.find_all('h1', 'heading-title')
        title = titleTag[0].string.strip()
        abstractTag = soup.find_all('div', 'abstract-content selected')
        abstractTag = abstractTag[0].find_all('p')
        if len(abstractTag) == 1:
            abstract = abstractTag[0].string.strip()
            abstractLists.append(('pmid: '+str(pmid),                                   'title: '+title,                                   'abstract: '+abstract))
    except AttributeError:
        pass

def saveContent():
    with open(path, 'wb') as f:
        f.write('The total number of articles: '.encode())
        f.write(str(len(abstractLists)).encode())
        f.write('\n\n'.encode())
        for Num, abstract in enumerate(abstractLists):
            for i in abstract:
                f.write(i.encode())
                f.write('\n'.encode())
            print('\r保存进度: {:.2f}%'.format((Num+1) * 100 / len(abstractLists)), end='')
            f.write('\n\n'.encode())
        f.close()
        print('文件保存成功！')

def main():
    startTime = time.time()
    if not os.path.exists(path):
        html = getHtmlText(base+middle+keyword)
        articleNum = parserArticleNum(html)
        
        pageNum = articleNum // 10 if articleNum % 10 == 0 else                                       articleNum // 10 + 1
        crawlPageNum = input('总页数: {0}, 输入爬取页数: '.format(pageNum))
        while not crawlPageNum.isdigit() or int(crawlPageNum) > pageNum:
            crawlPageNum = input('总页数: {0}, 输入爬取页数: '.format(pageNum))
        for i in range(1, int(crawlPageNum)+1):
            html = getHtmlText(base+middle+keyword+'&page='+str(i))
            parserMainHtmlText(html)
            print('\r爬取进度: {:.2f}%'.format(i * 100 / (int(crawlPageNum))), end='')        
        for Num, pmid in enumerate(pmidLists):
            html = getHtmlText(base+pmid)
            parserPmidHtmlText(html, pmid)
            print('\r解析进度: {:.2f}%'.format((Num+1) * 100 / len(pmidLists)), end='')
        saveContent()
        endTime = time.time()
        print('耗时: {0:.2f}s'.format(endTime-startTime))
    else:
        print('文件已存在！')

base = 'https://pubmed.ncbi.nlm.nih.gov/'
middle = '?term='
keyword = 'BVDV'
pmidLists = []
abstractLists = []
path = r'C:\Users\LV\Desktop\BVDV.txt'

if __name__ == '__main__':
    main()

