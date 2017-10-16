# -*- coding: utf-8 -*-
 
import os
from ucloud.ufile import getufilelist
from ucloud.compact import b
from ucloud.logger import logger, set_log_file
import ucloud.ufile.config as config
from ucloud.compact import BytesIO
import requests

from sdk.config_prod import *
 
set_log_file()
public_key = PUBLIC_KEY #添加自己的账户公钥
private_key = PRIVATE_KEY #添加自己的账户私钥
 
if __name__ == '__main__':
 
    # 构造对象，并设置公私钥
    handler = getufilelist.GetFileList(public_key, private_key)
 
    # 目标空间
    bucket = "mf23"
    # 设置每页的数量
    mylimit = 20
 
    # 获取第一页
    ret, resp = handler.getfilelist(bucket, limit=mylimit)
    assert resp.status_code == 200
    print("count:%d" % len(ret['DataSet']))
    for item in ret['DataSet']:
        print item
 
    # 若仍有后续内容, 继续翻页获取
    while ret['NextMarker'] != "":
        ret, resp = handler.getfilelist(bucket, limit=mylimit, marker=ret['NextMarker'])
        assert resp.status_code == 200
        print("count:%d" % len(ret['DataSet']))
        for item in ret['DataSet']:
            print item