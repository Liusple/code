#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser
import logging

#Ö÷ÕÊºÅ
accountSid= '8aaf0708568d4143015697b0f4960888';

#Ö÷ÕÊºÅToken
accountToken= '42d3191f0e6745d6a9ddc6c795da0bed';

#Ó¦ÓÃId
appId='8aaf0708568d4143015697b0f56e088f';

#ÇëÇóµØÖ·£¬¸ñÊ½ÈçÏÂ£¬²»ÐèÒªÐ´http://
serverIP='app.cloopen.com';

#ÇëÇó¶Ë¿Ú 
serverPort='8883';

#REST°æ±¾ºÅ
softVersion='2013-12-26';

# ·¢ËÍÄ£°å¶ÌÐÅ
# @param to ÊÖ»úºÅÂë
# @param datas ÄÚÈÝÊý¾Ý ¸ñÊ½ÎªÊý×é ÀýÈç£º{'12','34'}£¬Èç²»ÐèÌæ»»ÇëÌî ''
# @param $tempId Ä£°åId

# def sendTemplateSMS(to,datas,tempId):
#
#
#     #³õÊ¼»¯REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems():
#
#         if k=='templateSMS' :
#                 for k,s in v.iteritems():
#                     print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)


class CCP(object):

    def __init__(self):
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    @staticmethod
    def instance():
        if not hasattr(CCP, "_instance"):
            CCP._instance = CCP()
        return CCP._instance

    def sendTemplateSMS(self, to, datas, tempId):
        try:
            result = self.rest.sendTemplateSMS(to, datas, tempId)
        except Exception as e:
            logging.error(e)
            raise e

        # print result
        # for k, v in result.iteritems():
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
        if result.get("statusCode") == "000000":
            return True
        else:
            return False

ccp = CCP.instance()

if __name__ == "__main__":
    ccp = CCP.instance()
    ccp.sendTemplateSMS("18267170462", ["1234", 5], 1)



   
#sendTemplateSMS(ÊÖ»úºÅÂë,ÄÚÈÝÊý¾Ý,Ä£°åId)