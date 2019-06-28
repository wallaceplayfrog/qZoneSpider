import json
import os


class exactData(object):
    #定义从结果中获取我的QQ好友数据的方法，从结果中获取我的动态数据

    def __init__(self):
        print("开始从getFriends的结果提取qqnumber")

    def exactNumber(self):
        #从json中获取qqnumber
        friendsFiles = [x for x in os.listdir('friends') if x.endswith("json")]
        #print(len(friendsFiles))
        qqnumberItem = []
        i = 0
        for eachFile in friendsFiles:
            with open('friends/' + eachFile, encoding='utf-8') as f:
                source = f.read()
                conDict = source[75:-4].replace('\n', '')
                conJson = json.loads(conDict)
                friendsList = conJson['uinlist']

                # 从好友列表中获取每个元素用字典存储
                for item in friendsList:
                    i = i + 1
                    qqnumberItem.append(item)
        else:
            with open('qqnumber.inc', 'w', encoding='utf-8') as qqFile:
                print('好友数量:\t', len(qqnumberItem))
                qqFile.write(str(qqnumberItem))
        print('Finish!')