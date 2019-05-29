"""
把包含动态的文件下载下来
"""


import requests
import os
import sys
import time
import util


class Moods(object):
    '''用cookies获取动态文件'''

    def __init__(self):
        self.session = requests.Session()
        self.headers = util.headers
        self.g_tk = util.g_tk

    def getMoods(self, qqnumber):
        '''下载动态文件并保存到/mood_result/qqnumber文件夹下'''

        referer = 'http://user.qzone.qq.com/' + qqnumber
        self.headers['Referer'] = referer

        # 创建qqnumber夹用于保存文件
        util.checkPath('mood_result/' + qqnumber)

        # 获取目标url
        urlBase = util.parseMoodsUrl(qqnumber)

        pos = 0
        key = True

        while key:
            print("\tDealing with position:\t%d" % pos)
            url = url_base + "&pos=%d" % pos
            # print(url) 用于调试
            res = self.session.get(url, headers = self.headers)
            con = res.text
            with open('mood_result/' + qqnumber + '/' + str(pos), 'w', encoding="utf-8") as f:
                f.write(con)

            if '''"msglist":null''' in con:
                key = False

            # 禁止访问时
            if '''"msgnum":0''' in con:
                with open('naida_log.log', 'a', encoding="utf-8") as logFile:
                    logFile.write("%s Cannot access..\n" % qqnumber)
                key = False

            # Cookie 过期
            if '''"subcode":-4001''' in con:
                with open('naida_log.log', 'a', encoding="utf-8") as log_file:
                    log_file.write('Cookie Expried! Time is %s\n' % time.ctime())
                sys.exit()

            pos += 20
            time.sleep(5)

class moodsStart(object):

    def __init__(self):
        print('Start to get all friend\'s mood file and save it to the mood_result folder')

    def getMoodsStart(self):
        app = Moods()

        with open('qqnumber.inc', encoding="utf-8") as qnumberFile:
            qnumberString = qnumberFile.read()
        qnumberList = eval(qnumberString)

        # 检查文件夹是否存在
        # 不存在则创建
        util.checkPath('mood_result')

        while qnumberList != []:
            saveBackqNumber = qnumberList[:]
            item = qnumberList.pop()
            qq = item['data']
            print("Dealing with:\t%s" % qq)

            startTime = time.ctime()
            with open('naida_log.log', 'a', encoding="utf-8") as log_file:
                log_file.write("Program run at: %s\tGetting %s data...\n" % (startTime, qq))

            try:
                app.getMoods(qq)
            except KeyboardInterrupt:
                print('User Interrupt, program will exit')
                sys.exit()
            except Exception as e:
                # Write the rest item back to qqnumber.inc
                with open('qqnumber.inc', 'w', encoding="utf-8") as qnumberFile:
                    qnumberFile.write(str(saveBackqNumber))

                # 记录日志
                with open('naida_log.log', 'a', encoding="utf-8") as logFile:
                    exceptionTime = time.ctime()
                    logFile.write("Exception occured: %s\n%s\n" % (exceptionTime, e))
            else:
                print("%s Finish!" % qq)
        else:
            print("Finish All!")
