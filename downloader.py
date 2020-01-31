#最好用的一个
# coding:utf-8
import requests
import os
import re
# import json
import itertools
import urllib
import sys

# 百度图片URL解码
# http://blog.csdn.net/hbuxiaoshe/article/details/44780653
str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}
char_table = {ord(key): ord(value) for key, value in char_table.items()}

# 解码
def decode(url):
    for key, value in str_table.items():
        url = url.replace(key, value)
    return url.translate(char_table)

# 百度图片下拉
def buildUrls(word):
    word = urllib.parse.quote(word)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls


re_url = re.compile(r'"objURL":"(.*?)"')

# 获取imgURL
def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls

# 下载图片
def downImgs(imgUrl, dirpath, imgName, imgType):
    filename = os.path.join(dirpath, imgName)
    try:
        res = requests.get(imgUrl, timeout=15)
        if str(res.status_code)[0] == '4':
            print(str(res.status_code), ":", imgUrl)
            return False
    except Exception as e:
        print('抛出异常:', imgUrl)
        print(e)
        return False
    with open(filename + '.' + imgType, 'wb') as f:
        f.write(res.content)
    return True

# 创建文件路径
def mkDir(dirName):
    dirpath = os.path.join(sys.path[0], dirName)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath


if __name__ == '__main__':


    with open('m.txt', 'r', encoding="utf-8") as f:
        result = f.read()
    keys = result.split('\n')
    key_words = list(enumerate(keys, start=1))

    for key in key_words:
        word = key[1]

        dirpath = mkDir(word)

        imgType = 'jpg'
        strtag = word
        numIMGS = 3
        urls = buildUrls(word)
        index = 0
        #print("= = " * 25)
        for url in urls:
            print("正在请求：", url)
            html = requests.get(url, timeout=10).content.decode('utf-8')
            imgUrls = resolveImgUrl(html)
            # print(imgUrls)
            if len(imgUrls) == 0:  # 没有图片则结束
                break
            for url in imgUrls:
                if downImgs(url, dirpath, strtag + ' ' + str(index + 1), imgType):
                    index += 1
                    # print("已下载 %s 张" % index)
                    # 双 break 跳出下载循环
                if index == numIMGS:
                    break
            if index == numIMGS:
                # print('您一共下载了 %s 张图片' % index)
                # print('程序正在终止')
                break