# -*- coding: utf-8 -*-
 
import os
from ucloud.ufile import downloadufile
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
    # 两种下载方式:
    # 1. 通过下载对象类的方法函数下载
    # 2. 通过url下载
 
    # 构造下载对象，并设置公私钥
    handler = downloadufile.DownloadUFile(public_key, private_key)
 
    # 目标空间
    bucket = "mf23"
    # 目标空间内要下载的文件名
    key = "/tmp/ucloud/norun/111-1122-3233.sfs"
    # 文件下载到本地的保持路径
    save_file = "./111-1122-3233.sfs"
 
    # 通过对象类的方法函数请求下载
    ret, resp = handler.download_file(bucket, key, save_file, isprivate=True)
    assert resp.status_code == 200
 
    # 通过url下载，可设置url的过期时间(单位:秒)
    url = handler.private_download_url(bucket, key, expires=60)
    print(url)
    ret = requests.get(url)
    ret.BytesIO
    assert ret.status_code == 200
    # 之后根据实际的业务逻辑处理返回结果中的文件内容

