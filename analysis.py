import sqlite3
import time
import json
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def getAccessInfo():
    infopath = 'Access.json'
    try:
        with open(infopath, 'r', encoding = 'utf-8') as f:
            accessInfo = json.load(f)
        return accessInfo
    except:        
        print("Error: File Not Found==============")
        print("请检查配置文件是否正确配置!!!!")
        print("Please check config file")
        print("Path:", infopath)
        exit(1)

def getUsername():
    infopath = 'userinfo.json'
    try:    
        with open(infopath, 'r', encoding = 'utf-8') as r:
            userinfo = json.load(r)
        return userinfo["username"]
    except:
        print("Error: File Not Found==============")
        print("请检查配置文件是否正确配置!!!!")
        print("Please check config file")
        print("Path:", infopath)
        exit(1)

def overView():
    conn = sqlite3.connect('moods.sqlite')
    cur = conn.cursor()
    print('database successfully opened')

    cursor = cur.execute('SELECT MAX(id) FROM moods')
    for i in cursor:
        moodsCount = i
    moodsCount = str(moodsCount)
    moodsCount = moodsCount.strip('(,)')

    username = getUsername()
    accessInfo = getAccessInfo()
    print('\n******************\n爬取用户：{}'.format(username))
    print('一共为你爬取了{}名好友的{}条动态'.format(len(accessInfo), moodsCount))
    
    noAccessCount = 0
    for value in accessInfo.values():
        if value == 'False':
            noAccessCount += 1
    if noAccessCount > 0:
        print('扎心了，有{}位好友屏蔽了你的访问权限\n****************\n'.format(noAccessCount))
    else:
        print('牛bee所有的好友都可以访问\n******************\n')
    
    timedict = {'morning':0, 'noon-afternoon':0, 'evening':0, 'midnight':0}
    cursor = cur.execute('SELECT ctime FROM moods')
    print('你的好友动态发布的时间分布为如图：')
    getPostTime(cursor, timedict)
    
    print('\n输入好友qq查看说说词云图:') 
    qqnumber = input('>')
    checkNum(qqnumber, accessInfo)
    cursor = cur.execute('SELECT content From moods WHERE qq = {} '.format(qqnumber))
    text = ''
    for row in cursor:
        text += row[0]
    getWordCloud(text, qqnumber)

    while True:
        print('还想继续看？继续输入：(qqnumber/n)')
        qqnumber = input('>')
        if qqnumber == 'n':
            break
        checkNum(qqnumber, accessInfo)
        cursor = cur.execute('SELECT content From moods WHERE qq = {} '.format(qqnumber))
        text = ''
        for row in cursor:
            text += row[0]
        getWordCloud(text, qqnumber)
    print('Thanks for using')
    conn.close()

def checkNum(qqnumber, accessInfo):
    while True:
        if qqnumber not in accessInfo.keys():
            print('你确定你有这个好友？再输一个试试？')
            qqnumber = input('>')
        elif accessInfo[qqnumber] == 'False':
            print('人品太差了，TA的空间不给你看，再输一个试试？')
            qqnumber = input('>')
        elif accessInfo[qqnumber] == 'True':
            break


def getWordCloud(text, qq):
    fontpath = 'SIMYOU.TTF'
    cuttext = " ".join(jieba.cut(text))
    wordcloud = WordCloud(
        # 设置字体or乱码
        fontpath,
        # 设置背景，宽高
        background_color="white", width=2000, height=1380).generate(cuttext)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title('your friend {}'.format(qq))
    plt.axis("off")
    plt.show()
    
def getPostTime(cursor, timedict):
    for t in cursor:
        if 5 < int(time.ctime(t[0])[11:13]) <= 11:
            timedict['morning'] += 1
        elif 11 < int(time.ctime(t[0])[11:13]) <= 17:
            timedict['noon-afternoon'] += 1
        elif 17 < int(time.ctime(t[0])[11:13]) <= 23:
            timedict['evening'] += 1
        elif 0 <= int(time.ctime(t[0])[11:13]) <= 5:
            timedict['midnight'] += 1
    labels = 'morning(6-11)', 'daytime(12-17)', 'evening(18-23)', 'midnight(0-5)'
    fracs = [timedict['morning'], timedict['noon-afternoon'], timedict['evening'], timedict['midnight']]
    plt.axes(aspect=1)
    plt.title('moods time distribution')
    plt.pie(x=fracs, labels=labels, autopct='%3.1f %%', shadow=True, labeldistance=1.1, startangle = 90, pctdistance = 0.6)
    plt.show()

if __name__ == "__main__":
    overView()