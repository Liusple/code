# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem

#scrapy startproject weather
#scrapy genspider HQUSpider quanzhou.tianqi.com
#scrapy crawl HQUSpider
class HquspiderSpider(scrapy.Spider):
	name = 'HQUSpider'
	allowed_domains = ['tianqi.com']
	citys = ["quanzhou"]
	start_urls = []
	for city in citys:
		start_urls.append("http://" + city + ".tianqi.com/")

	def parse(self, response):
		#xpath?
		subSelector = response.xpath("//div[@class='tqshow1']")
		#[<Selector xpath="//div[@class='tqshow1']" data='<div class="tqshow1"><h3>泉州<font color="'>, <Selector xpath="//div[@class='tqshow1']" data='<div class="tqshow1"><h3>泉州<font color="'>, <Selector xpath="//div[@class='tqshow1']" data='<div class="tqshow1"><h3>泉州<font color="'>, <Selector xpath="//div[@class='tqshow1']" data='<div class="tqshow1"><h3>泉州14日天气</h3><p>'>, <Selector xpath="//div[@class='tqshow1']" data='<div class="tqshow1"><h3>泉州15日天气</h3><p>'>, <Selector xpath="//div[@class='tqshow1']" data='<div class="tqshow1"><h3>泉州16日天气</h3><p>'>]
		print("#########subSelector########:", subSelector)
		items = []
		'''
			<div class="tqshow1">
			<h3>泉州<font color="#0066cc">今日</font>天气</h3>
			<p>星期三</p>
			<ul>
			<li class="tqpng"><img class='pngtqico' align='absmiddle' src='http://img.tianqi.com/static/images/tianqibig/b1.png' style='border:0;width:46px;height:46px'/></li>
			<li><font color="#f00">33℃</font>~<font color="#4899be">25℃</font></li>
			<li>多云</li>
			<li style="height:18px;overflow:hidden">东北风 4级</li>
			</ul>
			</div>
		'''
		for sub in subSelector:
			item = WeatherItem()
			cityDates = ""
			for cityDate in sub.xpath("./h3//text()").extract():
				cityDates += cityDate  #泉州今日天气
			item["cityDate"] = cityDates
			item["week"] = sub.xpath("./p//text()").extract()[0] #星期三
			item["img"] = sub.xpath("./ul/li[1]/img/@src").extract()[0] #http://img.tianqi.com/static/images/tianqibig/b1.png
			temps = ""
			for temp in sub.xpath("./ul/li[2]//text()").extract():
				temps += temp
			item['temperature'] = temps  #33℃~25℃
			item['weather'] = sub.xpath('./ul/li[3]//text()').extract()[0]
			item['wind'] = sub.xpath('./ul/li[4]//text()').extract()[0]
			items.append(item)
			print(items)
		return items

