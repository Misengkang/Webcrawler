# -*- coding:utf-8 -*-
# !/usr/bin/env python


import requests
from bs4 import BeautifulSoup
import codecs  # 方便中文编码
import re

download_url = "http://movie.douban.com/top250"
movie_list = []


# 下载源码
def download_page(url):
    data = requests.get(url).content  # content 返回其他数据类型，图片二进制，字节流
    return data


# 解析源码
def parse_html(html):  # 接受html源码为输入，html用request.text或urllib.open打开

    soup = BeautifulSoup(html, "lxml")
    movie_list_soup = soup.find("ol", {"class": "grid_view"})

    for movie_li in movie_list_soup.findAll("li"):
        movie_em = movie_li.find("div", {"class": "pic"}).find("em").get_text()

        detail = movie_li.find("div", {"class": "hd"})
        movie_name = detail.find("span", {"class": "title"}).get_text()

        detail2 = movie_li.find("div", {"class": "star"})
        movie_score = detail2.find("span", {"class": "rating_num"}).get_text()
        movie_numbers = detail2.find(text=re.compile("[0-9]*人评价"))

        movie_250 = [movie_em + "--" + movie_name + "--" + movie_score + "--" + movie_numbers]
        movie_list.append(movie_250)

    next_page = soup.find("span", {"class": "next"}).find("a")
    if next_page:
        next_page_url = download_url + next_page["href"]
        s = download_page(next_page_url)
        parse_html(s)
    return movie_list


# 数据存储
def main():
    url = download_url
    html = download_page(url)
    movies = parse_html(html)
    with codecs.open('movies250.txt', 'wb', encoding='utf-8') as fp:
        for m in movies:
            fp.write(u'{movies}\n'.format(movies='\n'.join(m)))


# 程序入口
if __name__ == "__main__":  # 当模块被直接运行时，以下代码块将被运行，被导入时，不被运行
    main()
