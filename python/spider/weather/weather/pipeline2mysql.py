import MySQLdb
import os.path

class WeatherPipeline(object):
	def process_item(self, item, spider):
		cityDate = item["cityDate"]
		week = item["week"]
		temperature = item["temperature"]
		weather = item["weather"]
		wind = item["wind"]
		img = item["img"]
		conn = MySQLdb.connect(
				host = "ip",
				port = 3306,
				user = "",
				passwd = "scrapyDB",
				db = "",
				charset = "utf8"
			)
		cur = conn.cursor()
		cur.execute("INSERT weather(cityDate, week, img, temperature, weather, wind) values(%s,%s,%s,%s,%s,%s)", (cityDate, week, img, temperature, weather, wind))
		cur.close()
		conn.commit()
		conn.close()
		return item
