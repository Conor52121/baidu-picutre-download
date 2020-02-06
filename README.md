# BaiduPictureDownload
可以批量下载百度图片

使用环境：
    Python3.7

使用方法：
    先将所需要批量下载的图片的名称写在list.txt里面，将list.txt和downloader.py放在同一个目录下面，然后运行downloader.py即可。

with open('list.txt', 'r', encoding="utf-8") as f:

在此处可以修改所需下载的图片的文本文件的名字。

imgType = 'jpg'

在此处可以修改所需下载图片的格式。

numIMGS = 3

在此处可以修改每个图片名称下载图片的数量。

pachongceshi.exe为打包软件，将程序以及所有所需的依赖包封装为可执行文件，可以直接使用。可执行文件里面会有步骤提示如何一步步操作。
