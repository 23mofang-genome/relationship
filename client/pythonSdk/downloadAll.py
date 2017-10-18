# -*- coding: utf-8 -*-
 
import os
from ucloud.ufile import downloadufile, getufilelist
from ucloud.compact import b
from ucloud.logger import logger, set_log_file
import ucloud.ufile.config as config
from ucloud.compact import BytesIO
import requests

from sdk.config_prod import *
set_log_file()
public_key = PUBLIC_KEY #添加自己的账户公钥
private_key = PRIVATE_KEY #添加自己的账户私钥

import gevent.pool  
import gevent.monkey
gevent.monkey.patch_all()

def get_ufile_list(file_name_start_with):
    # 构造对象，并设置公私钥
    handler = getufilelist.GetFileList(public_key, private_key)
 
    # 目标空间
    bucket = "mf23"
    # 设置每页的数量
    mylimit = 1000
 
    # 获取第一页
    ret, resp = handler.getfilelist(bucket, limit=mylimit)
    assert resp.status_code == 200
    print("count:%d" % len(ret['DataSet']))

    # 保存最终结果
    result = []

    # 先取 1000 个
    for item in ret['DataSet']:
        if item['FileName'].startswith(file_name_start_with):
            result.append(item['FileName'])

    # 若仍有后续内容, 继续翻页获取
    while ret['NextMarker'] != "":
        ret, resp = handler.getfilelist(bucket, limit=mylimit, marker=ret['NextMarker'])
        assert resp.status_code == 200
        print("count:%d" % len(ret['DataSet']))
        for item in ret['DataSet']:
            if item['FileName'].startswith(file_name_start_with):
                result.append(item['FileName'])
    return result

# 设置协程池最大值
PoolNum = 20
def download_ufile_by_name_list(file_name_list):
    # 构造下载对象，并设置公私钥
    handler = downloadufile.DownloadUFile(public_key, private_key)
    # 目标空间
    bucket = "mf23"
    # 目标空间内要下载的文件名
    key = "/tmp/ucloud/norun/111-1117-2081.sfs"
    # 文件下载到本地的保持路径
    save_file = "/tmp/ucloud/norun/111-1117-2081.sfs"
    
    pool = gevent.pool.Pool(PoolNum)
    # 通过对象类的方法函数请求下载
    handler.download_file(bucket, key, save_file, isprivate=True)
    def worker(file_name):
        handler.download_file(bucket, file_name, file_name, isprivate=True)

    data = pool.map(worker, file_name_list)

if __name__ == "__main__":
    rt = get_ufile_list(file_name_start_with='/tmp/ucloud/norun/')
    print len(rt)
    download_ufile_by_name_list(rt)
