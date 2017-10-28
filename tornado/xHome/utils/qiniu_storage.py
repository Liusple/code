# -*- coding: utf-8 -*-

import qiniu.config
import logging

from qiniu import Auth, put_data, etag, urlsafe_base64_encode

#需要填写你的 Access Key 和 Secret Key
access_key = '5JS-pETy62A3YTqgzhn6MVp6yl4yt5XJCQqCctHA'
secret_key = 'SO4SCqTZ-fQNGN3HU7mhthoFUrL5DNNKxmkDR9tZ'

def storage(file_data):
    try:
        #构建鉴权对象
        q = Auth(access_key, secret_key)

        #要上传的空间
        bucket_name = 'ihome'

        #上传到七牛后保存的文件名
        # key = 'my-python-logo.png';


        #生成上传 Token，可以指定过期时间等

        token = q.upload_token(bucket_name)

        #要上传文件的本地路径
        # localfile = './sync/bbb.jpg'
        # ret, info = put_file(token, key, localfile)
        ret, info = put_data(token, None, file_data)
    except Exception as e:
        logging.error(e)
        raise e
    logging.debug(ret) #{u'hash': u'FkA586VxbgAfEaN5etO20VjA1qnV', u'key': u'FkA586VxbgAfEaN5etO20VjA1qnV'}
    logging.debug(info)#exception:None, status_code:200, _ResponseInfo__response:<Response [200]>, text_body:{"hash":"FkA586VxbgAfEaN5etO20VjA1qnV","key":"FkA586VxbgAfEaN5etO20VjA1qnV"}, req_id:WwcAAPAeaRoNTu4U, x_log:body;s.ph;s.put.tw;s.put.tr;s.put.tw;s.put.tr:1rs36_5.sel:4;rwro.ins:4/same entry;rs36_5.sel:15;rwro.get:15;MQ;RS.not:;RS:21;rs.put:22;rs-upload.putFile:30;UP:30[I 171017 16:25:43 qiniu_storage:40] image:FkA586VxbgAfEaN5etO20VjA1qnV upload succes
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)
    if 200 == info.status_code:
        logging.info("image:%s upload success" %ret["key"])
        return ret["key"]
    else:
        logging.info("image upload failed")
        raise Exception("上传失败")


if __name__ == "__main__":
    file_name = raw_input("input file name")
    with open(file_name, "rb") as file:
        file_data = file.read()
        storage(file_data)