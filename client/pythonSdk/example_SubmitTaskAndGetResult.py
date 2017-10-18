#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sdk import apiInterface
from sdk import tokenManager
import json
import time
import tarfile, io  
import sys

TestImageName="cn-bj2.ugchub.service.ucloud.cn/testbucket_two/relationship:0.1"

def untarbytes(data):
	tar = tarfile.open(fileobj=io.BytesIO(data))
	for member in tar.getmembers():
		f = tar.extractfile(member)
		print f.name 
		print f.read()


	    
if __name__=='__main__':
	tokenManager = tokenManager.TokenManager()
	token = tokenManager.getToken()

	print "example 1 submit sync task"
	STDIN=sys.stdin.read()
	print type(STDIN), len(STDIN)
	response = apiInterface.SubmitTask(ImageName=TestImageName, AccessToken=token, Cmd="", 
		  OutputDir="/tmp", OutputFileName="result", TaskType="Sync", TaskName="testsync", Data=STDIN)
	
	if isinstance(response,dict):
		print "submit sync task fail" + response["Message"]
	else:
		print "submit sync task success:" 
		print response
		print "untarbytes:" 
		untarbytes(response)
	print ""



	print "example 2 submit async task"
	response = apiInterface.SubmitTask(ImageName=TestImageName, AccessToken=token, Cmd="", 
		  OutputDir="/tmp", OutputFileName="result", TaskType="Async", TaskName="testasync", Data=STDIN)
	
	print response
	print ""

	if response["RetCode"] == 0:
		taskid = response["TaskId"]
	else:
		print "submit async task fail" + response["Message"]
	
	while True:
		response = apiInterface.GetTaskResult(TaskId=taskid, AccessToken=token)
		if isinstance(response,dict):
			print "GetTaskResult task fail " + response["Message"] + " " + response["State"]
		else:
			print "GetTaskResult success:" 
			print response
			print "untarbytes:" 
			untarbytes(response)
			break
		time.sleep(2)

