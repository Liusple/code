import re
from bs4 import BeautifulSoup
import urllib.request
from mylog import MyLog as mylog


class DoubleColorBallItem(object):
	date = None
	order = None
	red1 = None
	red2 = None
	red3 = None
	red4 = None
	red5 = None
	red5 = None 
	red6 = None
	blue = None
	monkey = None
	firstPrize = None
	secondPrize = None

class GetDoubleColorBallNumber(object):
	def __init__(self):
		#1)获取所有url
		#2)爬取所有url，取出需要数据
		self.urls = []
		self.log = mylog()
		self.getUrls()
		self.items = self.spider(self.urls)

	def getUrls(self):
		URL = r'http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html'
		htmlContent = self.getResponseContent(URL)
		soup = BeautifulSoup(htmlContent, 'lxml')
		tag = soup.find_all(re.compile("p"))[-1]
		'''
		<p class="pg"> 共<strong>109</strong> 页 /<strong>2171 </strong>条记录 <strong><a href="/zhcw/inc/ssq/ssq_wqhg.jsp">首页</a></strong> <strong><a href="/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum=1">上一页</a></strong> <strong><a href="/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum=2">下一页</a></strong> <strong><a href="/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum=109">末页</a></strong> 当前第<strong> 1 </strong>页</p> 
		'''
		self.log.info(tag)
		self.log.info(tag.attrs)
		pages = tag.strong.get_text() #109
		pages = 2 #for test
		self.log.info(pages)
		for i in range(1, int(pages)+1):
			url = r'http://kaijiang.zhcw.com/zhcw/html/ssq/list_'+str(i)+'.html'
			self.urls.append(url)
			self.log.info(url)

	def getResponseContent(self, url):
		try:
			response = urllib.request.urlopen(url)
		except:
			self.log.error("urllib open error")
		else:
			return response.read()


	def spider(self, urls):
		items = []
		for url in urls:
			htmlContent = self.getResponseContent(url)
			soup = BeautifulSoup(htmlContent, "lxml")
			tags = soup.find_all("tr", attrs={ })
			for tag in tags:
				if tag.find('em'):
					item=DoubleColorBallItem()
					tagTd=tag.find_all('td')
					item.date=tagTd[0].get_text()
					item.order=tagTd[1].get_text()
					tagEm=tagTd[2].find_all('em')
					item.red1=tagEm[0].get_text()
					item.red2=tagEm[1].get_text()
					item.red3=tagEm[2].get_text()
					item.red4=tagEm[3].get_text()
					item.red5=tagEm[4].get_text()
					item.red6=tagEm[5].get_text()
					item.blue=tagEm[6].get_text()
					item.money=tagTd[3].find('strong').get_text()
					item.firstPrize=tagTd[4].find('strong').get_text()
					item.secondPrize=tagTd[5].find('strong').get_text()
					items.append(item)
					self.log.info("%s: %s %s %s %s %s %s %s %s %s %s" %(item.date, item.red1, item.red2, item.red3, item.red4, item.red5, item.red6, item.blue, item.money, item.firstPrize, item.secondPrize))
		return items


if __name__ == "__main__":
	GDCBN = GetDoubleColorBallNumber()