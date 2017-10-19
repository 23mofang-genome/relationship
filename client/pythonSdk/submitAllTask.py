#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sdk import apiInterface
from sdk import tokenManager
import json
import time
import tarfile, io
import sys

import os, time
from downloadAll import get_ufile_list
import itertools
import gevent.pool
import gevent.monkey
from gevent import Timeout
import gzip, StringIO
gevent.monkey.patch_all()

TestImageName="cn-bj2.ugchub.service.ucloud.cn/testbucket_two/relationship:0.2.1"

def untarbytes(data):
    tar = tarfile.open(fileobj=io.BytesIO(data))
    for member in tar.getmembers():
        f = tar.extractfile(member)
        with open('result.txt','a') as result:
            strs = f.read()
            if strs.startswith('\n'):
                return
            else:
                result.write(strs)

def submit_worker(tuple_tow_file_name):
    first_file_name, second_file_name = tuple_tow_file_name
    first_file_name, second_file_name = os.path.basename(first_file_name), os.path.basename(second_file_name)
    with open("/data/norun/{0}".format(first_file_name)) as first:
        first = first.read()
        if not first:
            return
    with open("/data/run/{0}".format(second_file_name)) as second:
        second = second.read()
        if not first:
            return
    data = first + "separator" + second + "separator" + "{0}\n{1}".format(first_file_name, second_file_name)

    # 压缩
    stringf = StringIO.StringIO()
    zipper = gzip.GzipFile(mode = "wb", fileobj=stringf)
    zipper.write(data)
    zipper.close()
    try:
        with Timeout(10):
            # 提交任务
            response = apiInterface.SubmitTask(ImageName=TestImageName, AccessToken=token, Cmd="", OutputDir="/tmp", OutputFileName="result", TaskType="Sync", TaskName="testsync", Data=stringf)
        if isinstance(response, dict):
            print "submit sync task fail" + response["Message"]
        else:
            untarbytes(response)
    except Timeout:
        with open('timeout.txt','a') as timeoutf:
            strs = "<->".join(tuple_tow_file_name) + " TIMEOUT\n"
            timeoutf.write(strs)

if __name__=='__main__':
    length = len(sys.argv)
    if length == 2:
        PoolNum = int(sys.argv[1])
    else:
        sys.exit(-1)
    tokenManager = tokenManager.TokenManager()
    token = tokenManager.getToken()
    norun_list = get_ufile_list("/tmp/ucloud/norun/")
    run_list = get_ufile_list("/tmp/ucloud/run/")

    all_cuple = list(itertools.product(norun_list, run_list))

    PoolNum = PoolNum
    pool = gevent.pool.Pool(PoolNum)
    start = time.time()
    data = pool.map(submit_worker, all_cuple)
    stop = time.time()
    times = stop - start
    print times
    with open('time.txt', 'a') as time_file:
        time_file.write(times)