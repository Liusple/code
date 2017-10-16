#coding=utf-8
import os
from handlers.BaseHandler import StaticFileBaseHandler as StaticFileHandler
from handlers import Passport, VerifyCode#, Profile, House, Orders

urls = [
	#(r"/", Passport.IndexHandler),
	(r"/api/register", Passport.RegisterHandler)
	(r"/api/login", Passport.LoginHandler),
	(r"/api/logout", Passport.LogouHandler),
	(r"/api/check_login", Passport.CheckLoginHandler),
	(r"/api/piccode", VerifyCode.PicCodeHandler),
	(r"/api/smscode", VerifyCode.SMSCodeHandler),
	# (r"/api/register", Passport.RegisterHandler),
	# (r"/api/login", Passport.LoginHandler)
	(r"/(.*)", StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html"))
]