from bs4 import BeautifulSoup
import urllib.request
import re
import codecs
import time
from mylog import MyLog as mylog
#from save2mysql import SavebookData


class BookItem(object):
	categoryName = None
	middleUrl = None
	bookName = None
	wordsNum = None
	updateTime = None
	authorName = None

class GetBookName(object):
	def __init__(self):
		self.urlBase = "http://a.qidian.com/?action=1&orderId=&style=2&page=1"
		self.log = mylog()
		self.pages = self.getPages(self.urlBase)
		self.pages = 1 #for test
		print("pages:%s" %self.pages)
		self.booksList = []
		#将数据保存在list中
		self.spider(self.urlBase, self.pages)
		self.piplines(self.booksList)
		#self.log.info("begin save data to mysql\n")
		#SavebookData(self.booksList)
		#self.log.info("save data to mysql end...\n")

	#得到页数
	def getPages(self, url):
		print("begin to get pages")
		htmlContent = self.getResponseContent(url)
		soup = BeautifulSoup(htmlContent, "lxml")
		tags = soup.find('ul', attrs={"class":"lbf-pagination-item-list"})
		#self.log.info(type(tags)) #<class 'bs4.element.Tag'> 
		strUrl = tags.find_all("a")[-2].get("href") 
		#self.log.info(strUrl) #//www.qidian.com/all?action=1&orderId=&style=2&pageSize=50&siteid=1&hiddenField=0&page=753 
		self.log.info(strUrl.split("&"))  
		for st in strUrl.split("&"):
			if re.search('page=', st):
				pages = st.split("=")[-1] 
				self.log.info("page:%s" %pages)#753
				return int(pages)

	def getResponseContent(self, url):
		try:
			response = urllib.request.urlopen(url)
		except:
			self.log.error("failed:%s" %url)
		else:
			self.log.info("success:%s" %url)
			#print(response.read().decode("utf-8"))
			return response.read()

	def spider(self, url, pages):
		print("begin to spider")
		urlList = url.split("=")
		#self.log.info(urlList)
		for i in range(1, pages+1):
			#拼接为新的url
			urlList[-1] = str(i)
			newUrl = "=".join(urlList)
			#self.log.info(newUrl)
			htmlContent = self.getResponseContent(newUrl)
			soup = BeautifulSoup(htmlContent, "lxml")
			tags = soup.find("div", attrs={"class":"main-content-wrap fl"}).find("div", attrs={"class":"all-book-list"}).find("tbody").find_all("tr")
			'''
			<tr data-rid="1">
                <td class="td-one"><a class="type" href="//www.qidian.com/xuanhuan" data-eid="qd_B60" target="_blank"><em>「</em>玄幻</a><i class="point">&#183;</i><a class="go-sub-type" data-typeId="21" data-subtypeId="73" href="javascript:" data-eid="qd_B61">异世大陆<em>」</em></a></td>
                <td><a class="name" href="//book.qidian.com/info/2750457" data-bid="2750457" data-eid="qd_B58" target="_blank">大主宰</a></td>
                <td><a class="chapter" href="//vipreader.qidian.com/chapter/2750457/377224422" data-cid="//vipreader.qidian.com/chapter/2750457/377224422" data-bid="2750457" target="_blank">第一千五百五十一章邪神陨落（大结局）</a></td>
                <td><span class="total">496.03万</span></td>
                <td><a class="author" href="//my.qidian.com/author/1019021" target="_blank" data-eid="qd_B59">天蚕土豆</a></td>
                <td class="date">2017-07-08 21:02:53</td>
            </tr>
			'''

			for tag in tags:
				tds = tag.find_all("td")
				#self.log.info(tds)
				#self.log.info("\n")
				item = BookItem()
				item.categoryName = tds[0].find("a", attrs={"class":"type"}).get_text() + tds[0].find("a", attrs={"class": 'go-sub-type'}).get_text()
				item.middleUrl = tds[0].find("a", attrs={"class":"type"}).get("href")
				item.bookName = tds[1].find("a", attrs={"class":"name"}).get_text()

				item.wordsNum = tds[3].find("span", attrs={"class":"total"}).get_text()
				item.updateTime = tds[5].get_text()
				item.authorName = tds[4].find("a",attrs={"class":"author"}).get_text()
				self.booksList.append(item)
				#self.log.info("book info:%s %s %s %s" %(item.categoryName, item.bookName, item.wordsNum, item.authorName))

	def piplines(self, bookList):
		print("begin to wirte qidian.txt")
		bookName = "qidian.txt"
		nowTime = time.strftime('%Y-%m-%d %H:%M:%S \r\n',time.localtime())
		with codecs.open(bookName, "w", "utf8") as fp:
			fp.write("run at time:%s" %nowTime)
			for item in self.booksList:
				fp.write("{:<10} {:<20} {:<20} {:<20} {:<20}\r\n".format(item.categoryName, item.bookName, item.wordsNum, item.updateTime, item.authorName))
   
if __name__ == "__main__":
	GBN = GetBookName()












