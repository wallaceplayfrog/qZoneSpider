import requests
import os
import sys
import time
import util
import threading
import json

class Moods(object):
    #用cookies获取动态文件

    def __init__(self):
        self.session = requests.Session()
        self.headers = util.headers
        self.g_tk = util.g_tk
        self.access = self.getAccess()

    def getAccess(self):
        with open('Access.json', 'r', encoding='utf-8') as f:
            fstring = f.read()
        fjson = eval(fstring)
        return fjson

    def getMoods(self, qqnumber):
        #下载动态文件并保存到/mood_result/qqnumber文件夹下

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
            url = urlBase + "&pos=%d" % pos
            # print(url) 用于调试
            res = self.session.get(url, headers = self.headers)
            con = res.text
            with open('mood_result/' + qqnumber + '/' + str(pos), 'w', encoding="utf-8") as f:
                f.write(con)

            if '''"msglist":null''' in con:
                key = False

            # 禁止访问
            if '''"对不起,主人设置了保密,您没有权限查看"''' in con:
                with open('naida_log.log', 'a', encoding="utf-8") as logFile:
                    logFile.write("%s No access..\n" % qqnumber)
                self.access[qqnumber] = 'False'
                key = False
            else:
                self.access[qqnumber] = 'True'

            # Cookie 过期
            if '''"subcode":-4001''' in con:
                with open('naida_log.log', 'a', encoding="utf-8") as log_file:
                    log_file.write('Cookie expired! Time is %s\n' % time.ctime())
                sys.exit()

            pos += 20
            time.sleep(5)
        with open('Access.json', 'w', encoding = 'utf-8') as fp:
            fp.write((json.dumps(self.access, ensure_ascii = False, indent = 4)))
        

class moodsStart(object):

    def __init__(self):
        print('Start capturing all friend moods and store them in mood_result folder')

    def getMoodsStart(self):
        app = Moods()

        with open('qqnumber.inc', encoding="utf-8") as qnumberFile:
            qnumberString = qnumberFile.read()
        qnumberList = eval(qnumberString)

        # 检查文件夹是否存在
        # 不存在则创建
        util.checkPath('mood_result')
        self.sem = threading.Semaphore(10)
        while qnumberList != []:
            saveBackNumber = qnumberList[:]
            item = qnumberList.pop()

            self.sem.acquire()
            t = threading.Thread(target=self.getMooding, args=(item, app, saveBackNumber))
            t.start()
            time.sleep(1)
            
        else:
            print("Finish All!")
    
    def getMooding(self, item, app, saveBackNumber):
        #app = Moods()
        qq = item['data']
        print("Dealing with:\t%s" % qq)

        startTime = time.ctime()
        with open('naida_log.log', 'a', encoding="utf-8") as log_file:
            log_file.write("Program run at: %s\tGetting %s data...\n" % (startTime, qq))

        try:
            app.getMoods(qq)
        except KeyboardInterrupt:
            # 强制退出
            print('User Interrupt, program will exit')
        except Exception as e:
            # 将数据回写至qqnumber.inc
            with open('qqnumber.inc', 'w', encoding="utf-8") as qnumberFile:
                qnumberFile.write(str(saveBackNumber))

            # 记录日志
            with open('naida_log.log', 'a', encoding="utf-8") as logFile:
                exceptionTime = time.ctime()
                logFile.write("Exception occured: %s\n%s\n" % (exceptionTime, e))
        else:
            print("%s Finish!" % qq)
            self.sem.release()