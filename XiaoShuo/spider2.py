import os
import requests
from pyquery import PyQuery as pq
#使用的配置文件，而不是直接编进代码中
from config import *


def get_index_page(url):
    try:
        #关闭ssl校验
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url,verify=False)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except ConnectionError as e:
        print(e)

def parse_index_page(html):
    doc = pq(html)
    items = doc('#list dl dd').items()
    i = 0
    for item in items:
        # 去掉前十二个item
        if not i < 12:
            # 拿到章节链接
            link = item.find('a').attr('href')
            print(item.text() + '\t' + link)
            yield link,item.text()
        i += 1

def parse_chapter_text(html):
    doc = pq(html)
    items = doc('#content').items()
    for item in items:
        return item.text()


def get_chapter_page(url):
    try:
        #关闭ssl校验
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url,verify=False)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except ConnectionError as e:
        print(e)


def save_chapter(text,chapter_name,numbering):

    file_name = str(numbering) + chapter_name + '.txt'
    file_path = '{0}/{1}'.format(os.getcwd(),BOOK_NAME)
    mkdir(file_path)
    file_path = '{0}/{1}/{2}'.format(os.getcwd(), BOOK_NAME,file_name)
    try:
        with open(file_path,'w',encoding='utf-8') as f:
            f.write(text)
            print('保存' + chapter_name + ' 成功')
    except:
        print(chapter_name + '保存失败')


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


def main(book):
    html = get_index_page(START_URL+book)
    chapter_links = parse_index_page(html)
    numbering = 1
    for chapter_link,chapter_name in chapter_links:
        html = get_chapter_page(START_URL + chapter_link)
        text = parse_chapter_text(html)
        save_chapter(text,chapter_name,numbering)
        numbering += 1


if __name__ == '__main__':
    main(BOOK_CODE)