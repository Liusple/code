#coding=utf-8

import logging
import json
import constants
import math

from handlers.BaseHandler import BaseHandler
from utils.response_code import RET
from utils.commons import required_login
from utils.qiniu_storage import storage
from utils.session import Session


class AreaInfoHandler(BaseHandler):
	#where add area info??
	#/api/house/area
	def get(self):
		try:
			ret = self.redis.get("area_info")
		except Exception as e:
			logging.error(e)
			ret = None
		if ret:
			logging.info("hit redis: area_info")
			resp = '{"errcode":"0", "errmsg":"OK", "data":%s}' % ret
			return self.write(resp)
		sql = "select ai_area_id, ai_name from ih_area_info;"
		try:
			ret = self.db.query(sql)
			logging.debug(ret) #[{'ai_area_id': 1L, 'ai_name': u'jiading'}, {'ai_area_id': 3L, 'ai_name': u'jingan'}, {'ai_area_id': 4L, 'ai_name': u'minhang'}, {'ai_area_id': 5L, 'ai_name': u'pudong'}, {'ai_area_id': 6L, 'ai_name': u'xuhui'}]

		except Exception as e:
			logging.error(e)
			return self.write(dict(errcode=RET.NODATA, errmsg="db query falied"))
		if not ret:
			return self.write(dict(errcode=RET.NODATA, errmsg="没有数据"))
		data = []
		for row in ret:
			d = {
				"area_id": row.get("ai_area_id", ""),
				"name": row.get("ai_name", "")
			}
			data.append(d)
		json_data = json.dumps(data)
		try:
			self.redis.setex("area_info", constants.REDIS_AREA_INFO_EXPIRES_SECONDES, json_data)
		except Exception as e:
			logging.error(e)

		return self.write(dict(errcode=RET.OK, errmsg="Ok", data=data))

	'''
	/api/house/area
	{
		"areas": "beijing"
	}
	'''
	#地区应该唯一
	def post(self):
		area_name = self.json_args.get("area")
		if area_name in (None, ""):
			return self.write(dict(errcode=RET.PARAMERR, errmsg="param error"))
		sql = "insert into ih_area_info(ai_name) values(%(area_name)s);"
		try:
			self.db.execute(sql, area_name=area_name)  #must area_name=area_name
		except Exception as e:
			logging.error(e)
			return self.write(dict(errcode=RET.DATAERR, errmsg="insert db error"))
		self.write(dict(errcode=RET.OK, errmsg="OK"))


class MyHousesHandler(BaseHandler):
	#/api/house/my
	@required_login
	def get(self):
		user_id = self.session.data["user_id"]
		try:
			#"tail need blank"
			sql = "select a.hi_house_id, a.hi_title, a.hi_price, a.hi_ctime, b.ai_name, a.hi_index_image_url " \
			"from ih_house_info as a inner join ih_area_info as b on a.hi_area_id=b.ai_area_id where a.hi_user_id=%s;"
			ret = self.db.query(sql, user_id)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errcode=RET.DBERR, errmsg="get data erro"))

		houses = []
		if ret:
			for l in ret:
				house = {
					"house_id":l["hi_house_id"],
					"title":l["hi_title"],
					"price":l["hi_price"],
					"ctime":l["hi_ctime"].strftime("%Y-%m-%d"),
					"area_name":l["ai_name"],
					"img_url":constants.QINIU_URL_PREFIX + l["hi_index_image_url"] if l["hi_index_image_url"] else ""
				}
				houses.append(house)
		self.write({"errcode":RET.OK, "errmsg":"Ok", "houses":houses})


class HouseImageHandler(BaseHandler):
	'''
	/api/house/image
	house_id
	house_image
	'''
	@required_login
	def post(self):
		user_id = self.session.data["user_id"]
		house_id = self.get_argument("house_id")
		house_image = self.request.files["house_image"][0]["body"]
		img_name = storage(house_image)
		if not img_name:
			return self.write(dict(errcode=RET.THIRDERR, errmsg="qiniu error"))
		try:
			sql = "insert into ih_house_image(hi_house_id, hi_url) values(%s, %s);"\
				  "update ih_house_info set hi_index_image_url=%s " \
				  "where hi_house_id=%s and hi_index_image_url is null;"
			self.db.execute(sql, house_id, img_name, img_name, house_id)
		except Exception as e:
			logging.error(e)
			return self.write({"errcode":RET.DBERR, "errmsg":"upload failed"})
		img_url = constants.QINIU_URL_PREFIX + img_name
		self.write({"errcode":RET.OK, "errmsg":"Ok", "url":img_url})

#no
class IndexHandler(BaseHandler):
	def get(self):
		try:
			ret = self.redis.get("home_page_data")
		except Exception as e:
			logging.error(e)
			ret = None
		if ret:
			json_houses = ret
		else:
			try:
				house_ret = self.db.query("select hi_house_id, hi_title, hi_order_count, hi_index_image_url from ih_house_info" \
											"order by hi_order_count desc limit %s;" %constants.HOME_PAGE_MAX_HOUSES)
			#house_ret type???
			except Exception as e:
				logging.error(e)
				return self.write({"errcode":RET.DBERR, "errmsg":"get data error"})
			if not house_ret:
				return self.write({"errcode":RET.NODATA, "errmsg":"no data"})
			houses = []
			for l in house_ret:
				if not l["hi_index_image_url"]:
					continue
				house = {
					"house_id":l["hi_house_id"],
					"title":l["hi_title"],
					"img_url":constants.QINIU_URL_PREFIX + l["hi_index_image_url"]
				}
				houses.append(house)
			json_houses = json.dumps(houses)
			try:
				self.redis.setex("home_page_data", constants.HOME_PAGE_DATA_REDIS_EXPIRE_SECOND, json_houses)
			except Exception as e:
				logging.error(e)

			try:
				ret = self.redis.get("area_info")
			except Exception as e:
				logging.error(e)
				ret = None
			if ret:
				json_areas = ret
			else:
				try:
					area_ret = self.db.query("select ai_area_id, ai_name from ih_area_info")
				except Exception as e:
					logging.error(e)
					area_ret = None
				areas = []
				if area_ret:
					for area in area_ret:
						areas.append(dict(area_id=area["ai_area_id"], name=area["ai_name"]))
				json_areas = json.dumps(areas)
				try:
					self.redis.setex("area_info", constants.REDIS_AREA_INFO_EXPIRES_SECONDES, json_areas)
				except Exception as e:
					logging.error(e)
			# 1.dict->json.dumps
			# 2.str->dict
			resp = '{"errcode":"0", "errmsg":"OK", "houses":%s, "areas":%s}' %(json_houses, json_areas)
			self.write(resp)


class HouseInfoHandler(BaseHandler):
	'''
	/api/house/info
	{
		"user_id":"",
		"title":"",
		"price":"",
		"area_id":"",
		"address":"",
		"room_count":"",
		"acreage":"",
		"unit":"",
		"capacity":"",
		"beds":"",
		"deposit":"",
		"min_days":"",
		"max_days":"",
		"facility":[]
	}
	'''
	@required_login
	def post(self):
		user_id = self.session.data.get("user_id")
		title = self.json_args.get("title")
		price = self.json_args.get("price")
		area_id = self.json_args.get("area_id")
		address = self.json_args.get("address")
		room_count = self.json_args.get("room_count")
		acreage = self.json_args.get("acreage")   #房屋面积
		unit = self.json_args.get("unit")         #房屋户型
		capacity = self.json_args.get("capacity") #容纳人数
		beds = self.json_args.get("beds")
		deposit = self.json_args.get("deposit")   #押金 单位分
		min_days = self.json_args.get("min_days")
		max_days = self.json_args.get("max_days")
		facility = self.json_args.get("facility") #一个房屋的设施，是列表类型

		if not all((title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days)):
			return self.write(dict(errcode=RET.PARAMERR, errmsg="缺少参数"))
		try:
			price = int(price) * 100
			deposit = int(deposit) * 100
		except Exception as e:
			return self.write(dict(errcode=RET.PARAMERR, errmsg="deal price fail"))

		try:
			sql = "insert into ih_house_info(hi_user_id, hi_title, hi_price, hi_area_id, hi_address, hi_room_count," \
				  "hi_acreage, hi_house_unit, hi_capacity, hi_beds, hi_deposit, hi_min_days, hi_max_days) " \
				  "values(%(user_id)s, %(title)s, %(price)s, %(area_id)s, %(address)s, %(room_count)s, %(acreage)s, " \
				  "%(house_unit)s,%(capacity)s,%(beds)s,%(deposit)s,%(min_days)s,%(max_days)s);"

			house_id = self.db.execute(sql, user_id=user_id, title=title, price=price, area_id=area_id, address=address,
				room_count=room_count, acreage=acreage, house_unit=unit, capacity=capacity,
				beds=beds, deposit=deposit, min_days=min_days, max_days=max_days)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errcode=RET.DBERR, errmsg="save data error"))

		try:
			sql = "insert into ih_house_facility(hf_house_id, hf_facility_id) values"
			sql_val = []
			vals = []
			for facility_id in facility:
				sql_val.append("(%s, %s)") #['(%s, %s)', '(%s, %s)', '(%s, %s)', '(%s, %s)', '(%s, %s)', '(%s, %s)']
				vals.append(house_id)
				vals.append(facility_id)
			#vals:[111, 1, 111, 2, 111, 3, 111, 4, 111, 5, 111, 6]
			sql += ",".join(sql_val)#'insert into ih_house_facility(hf_house_id, hf_facility_id) values(%s, %s),(%s, %s),(%s, %s),(%s, %s)'
			vals = tuple(vals)
			logging.debug(sql)
			logging.debug(vals)
			self.db.execute(sql, *vals)
		except Exception as e:
			logging.error(e)
			try:
				self.db.execute("delete from ih_house_info where hi_house_id=%s", house_id)
			except Exception as e:
				logging.error(e)
				return self.write(dict(errcode=RET.DBERR, errmsg="delete fail"))
			else:
				return self.write(dict(errcode=RET.DBERR, errmsg="no data save"))
		self.write(dict(errcode=RET.OK, errmsg="OK", house_id=house_id)) ###care


	#/api/house/info?house_id=
	def get(self):
		session = Session(self) ##care
		user_id = session.data.get("user_id", "-1")
		house_id = self.get_argument("house_id")
		if not house_id:
			return self.write(dict(errcode=RET.PARAMERR, errmsg=""))
		try:
			ret = self.redis.get("house_info_%s" %house_id)
		except Exception as e:
			logging.error(e)
			ret = None
		if ret:
			resp = '{"errcode":"0", "errmsg":"OK", "data":%s, "user_id":%s}' %(ret, user_id)
			return self.write(resp)
		sql = "select hi_title, hi_price, hi_address, hi_room_count, hi_acreage, hi_house_unit, hi_capacity, hi_beds,"\
			  "hi_deposit, hi_min_days, hi_max_days, up_name, up_avatar, hi_user_id "\
			  "from ih_house_info inner join ih_user_profile on hi_user_id=up_user_id where hi_house_id=%s;"
		try:
			ret = self.db.get(sql, house_id)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errcode=RET.DBERR, errmsg="db get error"))
		if not ret:
			return self.write(dict(errcode=RET.NODATA, errmsg="no data get"))

		data = {
			"hid":house_id,
			"user_id":ret["hi_user_id"],
			"title":ret["hi_title"],
			"price":ret["hi_price"],
			"address":ret["hi_address"],
			"room_count":ret["hi_room_count"],
			"acreage":ret["hi_acreage"],
			"unit":ret["hi_house_unit"],
			"capacity":ret["hi_capacity"],
			"beds":ret["hi_beds"],
			"deposit":ret["hi_deposit"],
			"min_days":ret["hi_min_days"],
			"max_days":ret["hi_max_days"],
			"user_name":ret["up_name"],
			"user_avatar":constants.QINIU_URL_PREFIX + ret["up_avatar"] if ret.get("up_avatar") else ""
		}

		sql = "select hi_url from ih_house_image where hi_house_id=%s;"
		try:
			ret = self.db.query(sql, house_id)
		except Exception as e:
			logging.error(e)
			ret = None
		images = []
		if ret:
			for image in ret:
				images.append(constants.QINIU_URL_PREFIX + image["hi_url"])
		data["images"] = images

		sql = "select hf_facility_id from ih_house_facility where hf_house_id=%s;"
		try:
			ret = self.db.query(sql, house_id)
			#ret type
		except Exception as e:
			logging.error(e)
			ret = None
		facilities = []
		if ret:
			for facility in ret:
				facilities.append(facility["hf_facility_id"])
		data["facilities"] = facilities

		sql = "select oi_comment, up_name, oi_utime, up_mobile from ih_order_info inner join ih_user_profile " \
				"on oi_user_id=up_user_id where oi_house_id=%s and oi_status=4 and oi_comment is not null;"

		try:
			ret = self.db.query(sql, house_id)  ###care query
		except Exception as e:
			logging.error(e)
			ret = None
		comments = []
		if ret:
			for comment in ret: ##care ret
				comments.append(dict(
						user_name=comment["up_name"] if comment["up_name"]!=comment["up_mobile"] else "匿名用户",
						content=comment["oi_comment"],
						ctime=comment["oi_utime"].strftime("%Y-%m-%d %H:%M:%S")
					))
		data["comments"] = comments
		json_data = json.dumps(data)
		try:
			self.redis.setex("house_info_%s" %house_id, constants.REDIS_HOUSE_INFO_EXPIRES_SECONDES, json_data)
		except Exception as e:
			logging.error(e)
		resp = '{"errcode":"0", "errmsg":"OK", "data":%s, "user_id":%s}' %(json_data, user_id)
		self.write(resp)


class HouseListHandler(BaseHandler):
	pass


class HouseListRedisHandler(BaseHandler):
	pass