#coding=utf-8
from utils.response_code import RET
from utils.commons import required_login
from utils.qiniu_storage import storage
from .BaseHandler import BaseHandler

import constants
import logging

class AvatarHandler(BaseHandler):
	#/api/profile/avatar
	@required_login
	def post(self):
		files = self.request.files.get("avatar") ####
		#logging.debug(self.request.files)  #{u'file': [{'body':'','content_type': u'image/png', 'filename': u'qq.png'}]}
		if not files:
			return self.write(dict(errcode=RET.PARAMERR, errmsg="未传图片"))
		avatar = files[0]["body"]
		#logging.debug("AvatarHandler type(files):%s" %(type(files))) #<type 'list'>
		try:
			file_name = storage(avatar)
			logging.debug(file_name) #avatar
		except Exception as e:
			logging.error(e)
			return self.write(dict(errcode=RET.THIRDERR, errmsg="上传失败"))

		user_id = self.session.data["user_id"] #
		logging.debug(user_id)
		sql = "update ih_user_profile set up_avatar=%(avatar)s where up_user_id=%(user_id)s;"
		try:
			row_count = self.db.execute_rowcount(sql, avatar=file_name, user_id=user_id)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errcode=RET.DBERR, errmsg="保存错误"))
		#data:"http://oxy4g2gly.bkt.clouddn.com/FmyaPesgUtGf5K5lZaXUtBLd046f"
		self.write(dict(errcode=RET.OK, errmsg="保存成功", data="%s%s" % (constants.QINIU_URL_PREFIX, file_name)))


class ProfileHandler(BaseHandler):
	#/api/profile
	@required_login
	def get(self):
		user_id = self.session.data["user_id"]
		try:
			ret = self.db.get("select up_name, up_mobile, up_avatar from ih_user_profile where up_user_id=%s", user_id)
		except Exception as e:
			logging.error(e)
			return self.write(dict(errcode=RET.PARAMERR, errmsg=""))
		if ret["up_avatar"]:
			img_url = constants.QINIU_URL_PREFIX + ret["up_avatar"]
		else:
			img_url = None
		return self.write({"errcode":RET.OK, "errmsg":"OK", "data":{"user_id":user_id, "name":ret["up_name"], "mobile":ret["up_mobile"], "avatar":img_url}})


class AuthHandler(BaseHandler):
	"""实名认证"""
	#/api/profile/auth
	@required_login
	def get(self):
		user_id = self.session.data["user_id"]

		try:
			ret = self.db.get("select up_real_name,up_id_card from ih_user_profile where up_user_id=%s;", user_id)
		except Exception as e:
			logging.error(e)
			return self.write({"errcode":RET.DBERR, "errmsg":"get data failed"})
		logging.debug(ret) #{'up_id_card': None, 'up_real_name': None}
		if not ret:
			return self.write({"errcode":RET.NODATA, "errmsg":"no data"})
		self.write({"errcode":RET.OK, "errmsg":"OK", "data":{"real_name":ret.get("up_real_name", ""), "id_card":ret.get("up_id_card", "")}})

	'''
	/api/profile/auth
	{
		"real_name": "Alex",
		"id_card": "320xxxxxxx"
	}
	'''
	@required_login
	def post(self):
		user_id = self.session.data["user_id"]
		real_name = self.json_args.get("real_name")
		id_card = self.json_args.get("id_card")
		if real_name in (None, "") or id_card in (None, ""):
			return self.write({"errcode":RET.PARAMERR, "errmsg":"params error"})
		# 判断身份证号格式
		try:
			self.db.execute_rowcount("update ih_user_profile set up_real_name=%s, up_id_card=%s where up_user_id=%s", real_name, id_card, user_id)
		except Exception as e:
			logging.error(e)
			return self.write({"errcode":RET.DBERR, "errmsg":"update failed"})
		self.write({"errcode":RET.OK, "errmsg":"OK"})


class NameHandler(BaseHandler):
	"""设置用户名"""
	#/api/profile/name
	@required_login
	def post(self):
		# 从session中获取用户身份,user_id
		user_id = self.session.data["user_id"]
		name = self.json_args.get("name")

		# 判断name是否传了，并且不应为空字符串
		# if name == None or "" == name:
		if name in (None, ""):
			return self.write({"errcode":RET.PARAMERR, "errmsg":"params error"})

		# 保存用户昵称name，并同时判断name是否重复（利用数据库的唯一索引)
		try:
			self.db.execute_rowcount("update ih_user_profile set up_name=%s where up_user_id=%s", name, user_id)
		except Exception as e:
			logging.error(e)
			return self.write({"errcode":RET.DBERR, "errmsg":"name has exist"})

		# 修改session数据中的name字段，并保存到redis中 
		#care here
		self.session.data["name"] = name
		try:
			self.session.save()
		except Exception as e:
			logging.error(e)
		self.write({"errcode":RET.OK, "errmsg":"OK"})
