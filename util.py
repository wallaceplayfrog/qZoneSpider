'''
用到的工具函数、变量集合
'''

import os
import re
from urllib import parse
import requests


def getCookie():
    '''从已保存cookie_file读取cookie'''
    with open('cookie_file') as f:
        cookie = f.read()
    cookie = cookie.replace('\n', '')

    return cookie

cookie = getCookie()

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
    'accept-encoding': 'gzip, deflate, br',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'cookie': cookie,
    'connection': 'keep-alive'
}

def getGtk():
    '''获取g_tk加密参数'''

    pskeyStart = cookie.find('p_skey=')
    pskeyEnd = cookie.find(';', pskeyStart)

    # 有时 p_skey 会出现在 cookie 的最后，此时 pskey_end 会返回-1
    # 应该直接取到结束
    if pskeyEnd == -1:
        p_skey = cookie[pskey_start+7:]
    else:
        p_skey = cookie[pskey_start+7: pskey_end]

    h = 5381

    for s in p_skey:
        h += (h << 5) + ord(s)

    return h & 2147483647

g_tk = getGtk()


def getQzonetoken(qqnum):
    '''获取qzonetoken，它位于空间首页的源代码中'''
    indexUrl = "https://user.qzone.qq.com/%s" % qqnum
    headers['referer'] = 'https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone'
    headers['upgrade-insecure-requests'] = '1'
    res = requests.get(indexUrl, headers=headers)
    src = res.text
    searchRes = re.search(r'g_qzonetoken.*return\s*"(.*)";}', src, re.S)
    return searchRes.group(1) if searchRes else ''


def parseMoodsUrl(qqnum):
    '''获取每个好友的动态链接，需要提供他们的qqnumber来获取url
    '''

    params = {"cgi_host": "http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6",
              "code_version": 1,
              "format": "jsonp",
              "g_tk": g_tk,
              "hostUin": qqnum,
              "inCharset": "utf-8",
              "need_private_comment": 1,
              "notice": 0,
              "num": 20,
              "outCharset": "utf-8",
              "sort": 0,
              "uin": qqnum}
    host = "https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?"

    url = host + parse.urlencode(params)
    return url

def parseFriendsUrl():
    '''用cookie生成url，不需要提供qqnumber
    '''

    cookie = headers['cookie']
    qqStart = cookie.find('uin=o')
    qqEnd = cookie.find(';', qqStart)
    qqNumber = cookie[qqStart+5 : qqEnd]
    if qqNumber[0] == '0':
        qqNumber = qqNumber[1:]
    # 先获取qzonetoken
    qzonetoken = getQzonetoken(qqNumber)
    params = {"uin": qqNumber,
              "fupdate": 1,
              "action": 1,
              "g_tk": g_tk,
              "qzonetoken": qzonetoken}

    host = "https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/right/get_entryuinlist.cgi?"
    url = host + parse.urlencode(params)

    return url

def checkPath(path):
    '''检查路径是否存在
       否，则创建
    '''

    if not os.path.exists(path):
        os.mkdir(path)
