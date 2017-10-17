# pythonSdk for UCloud UGC

## Dependencies:
- requests

## Documents:
[产品文档][1]
[API文档][2]

[1]:https://docs.ucloud.cn/compute/ugc/index.html
[2]:https://docs.ucloud.cn/api/ugc-api/index

# UFile 相关文档

[官网文档](https://docs.ucloud.cn/storage_cdn/ufile/tools)
## 安装
从官网SDK页面下载Python-SDK源码，并解压

```
wget http://sdk.ufile.ucloud.com.cn/python_sdk.tar.gz
tar zxvf python_sdk.tar.gz
```
进入解压后的目录，进行安装

```
cd ufile-python
python setup.py install
```

> 详细的依赖和包结构，可参考ufile-python目录下的README.md文件。

然后就可以执行：

```shell
# 获取文件列表
python example_GetFileListFromUFile.py
# 下载一个文件
python example_GetFileFromUFile.py
```
