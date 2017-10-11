import re
from bs4 import BeautifulSoup
import urllib.requset
from mylog import Mylog as mylog


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
		self.urls = []
		self.log = mylog
		self.getUrls()
		#self.items = self.spider(self.urls)
		#self.pipelines(self.items)

	def getUrls(self):
		URL = r'http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html'
		htmlContent = self.getResponseContent(URL)
		soup = BeautifulSoup(htmlContent, 'lxml')
		tag = soup.find_all(re.compile("p"))[-1]
		self.log.info(tag)
		pages = tag.strong.get_text()
		self.log.info(pages)
		for i in range(1, int(pages)+1):
			url = r'http://kaijiang.zhcw.com/zhcw/html/ssq/list_'+str(i)+'.html'
			self.urls.append(url)
			self.log.info(url)

	def getResponseContent(self, url):
		try:
			response = urllib.requset.open(url)
		except:
			self.log.error("urllib open error")
		else:
			self.log.info("url open success")
			return response.read()
