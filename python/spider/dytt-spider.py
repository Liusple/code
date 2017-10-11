#coding=utf-8

import requests
import requests_cache
from bs4 import BeautifulSoup
import os
import time

'''
获取电影天堂首页电影的ftp路径
requests
select
'''
requests_cache.install_cache("demo_cache")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}

reponse = requests.get("http://www.dy2018.com/html/gndy/dyzz/index.html", headers=headers)
html_doc = reponse.content.decode("gbk")
#print(html_doc)

#<a href="/i/98435.html" class="ulink" title="2017年美国7.5分科幻片《蜘蛛侠：英雄归来》BD中英双字">2017年美国7.5分科幻片《蜘蛛侠：英雄归来》BD中英双字</a>
soup = BeautifulSoup(html_doc, "lxml")
links = []
for l in soup.select(".ulink"):              #select
	href = "http://www.dy2018.com" + l["href"]
	title = l.string #2017年美国7.5分科幻片《蜘蛛侠：英雄归来》BD中英双字">2017年美国7.5分科幻片《蜘蛛侠：英雄归来》BD中英双字
	links.append(href)
	print(href, title)
	
for link in links:
	reponse = requests.get(link, headers=headers)
	html_doc = reponse.content.decode("gbk")
	soup = BeautifulSoup(html_doc, "lxml")
	
	#soup.select("#Zoom table a")可能会存在是数组的情况，这里暂且取第一个
	#[<a href="ftp://z:z@dygod18.com:21211/[电影天堂www.dy2018.com]大护法HD高清国语中字.mkv">ftp://z:z@dygod18.com:21211/[电影天堂www.dy2018.com]大护法HD高清国语中字.mkv</a>]
	ftp_elememt = soup.select("#Zoom table a")[0]
	down_link = ftp_elememt["href"]
	print(down_link)
	time.sleep(1)