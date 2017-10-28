#coding=utf-8
import os
from handlers.BaseHandler import StaticFileBaseHandler as StaticFileHandler
from handlers import Passport, VerifyCode, Profile, House, Orders

urls = [
	(r"/api/test", Passport.TestHandler),
	(r"/api/register", Passport.RegisterHandler),
	(r"/api/login", Passport.LoginHandler),
	(r"/api/logout", Passport.LogoutHandler),
	(r"/api/check_login", Passport.CheckLoginHandler),
	(r"/api/piccode", VerifyCode.PicCodeHandler),
	(r"/api/smscode", VerifyCode.SMSCodeHandler),
	(r"/api/profile/avatar", Profile.AvatarHandler),
	(r"/api/profile/name", Profile.NameHandler),
	(r"/api/profile/auth", Profile.AuthHandler),
	(r"/api/profile", Profile.ProfileHandler),
	(r"^/api/house/info$", House.HouseInfoHandler),
	(r"^/api/house/area", House.AreaInfoHandler),
	(r"^/api/house/image$", House.HouseImageHandler),
	(r"^/api/house/index$", House.IndexHandler),
	(r'^/api/house/list$', House.HouseListHandler), # 房屋过滤列表数据
	(r'^/api/house/list2$', House.HouseListRedisHandler), # 房屋过滤列表数据
	(r"^/api/house/my$", House.MyHousesHandler),
	(r"^/api/order$", Orders.OrderHandler),
	(r"^/api/order/my$", Orders.MyOrdersHandler),
	(r"^/api/order/comment$", Orders.OrderCommentHandler),
	(r"^/api/order/accept$", Orders.AcceptOrderHandler),
	(r"^/api/order/reject$", Orders.RejectOrderHandler),
	(r"/(.*)", StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html"))
]