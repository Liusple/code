import MySQLdb

class SavebookData(object):
	def __init__(self, items):
		self.host = ""
		self.port = 3306
		self.user = ""
		self.passwd = ""
		self.db = "bs4DB"
		self.run(items)

	def run(self, items):
		conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset="utf-8")
		cur = conn.cursor()
		print("connect success")
		for item in items:
			cur.execute("INSERT INTO qiDianBooks(categoryName, bookName, wordsNum, updateTime, authorName) VALUES(%s,%s,%s,%s,%s)",
				(item.categoryName.encode("utf8"), item.bookName.encode("utf8"), item.wordsNum.encode("utf8"), item.updateTime("utf8"), item.authorName.encode("utf8")))
		cur.close()
		conn.commit()
		conn.close()

