import os
import json
import sqlite3
import html

class GetDetail(object):
    #清洗动态数据并存储到数据库

    def __init__(self, conn, cur):
        self.count = 0
        self.conn = conn
        self.cur = cur

    # 用于临时保存每个QQ的动态信息，QQ号为键，值为这个QQ号的所有动态的文件列表
    def makeDict(self):
        moodDict = dict()
        dirList = os.listdir('mood_result')
        for d in dirList:
            fileList = os.listdir('mood_result/' + d)
            if len(fileList) != 1:
                moodDict[d] = fileList
        return moodDict

    # 主要的功能函数，把动态信息从文件里提取出来，并调用insertToDB方法插入到sqlite数据库中
    def exactMoodData(self, qq, fname):
        #从result文件夹获取动态数据
        qqnumber = qq
        fileName = fname
        with open(fileName, encoding="utf-8") as f:
            con = f.read()
        conDict = json.loads(con[10:-2])
        try:
            moods = conDict['msglist']
        except KeyError:
            return
        if moods == None:
            return

        moodItem = dict()
        moodItem['belong'] = qqnumber

        for mood in moods:
            moodItem['content'] = mood['content']
            moodItem['create_time'] = mood['created_time']
            moodItem['comment_num'] = mood['cmtnum']
            moodItem['phone'] = mood['source_name']
            moodItem['pic'] = mood['pic'][0]['url2'] if 'pic' in mood else ''
            moodItem['locate'] = mood['story_info']['lbs']['name'] if 'story_info' in mood else ''

            if moodItem['content'] == '' and moodItem['pic'] != '':
                # 如果一个动态除了图片没别的
                moodItem['content'] = moodItem['pic']
            if moodItem['content'] == '' and 'rt_con' in mood:
                # 如果动态内容是一个转发的视频
                # 它会被保存在mood['rt_con']中
                try:
                    moodItem['content'] = mood['rt_con']['conlist'][0]['con']
                except IndexError:
                    moodItem['content'] = mood['rt_con']['conlist'][1]['con']
                except KeyError:
                    # 当一个动态含有链接
                    moodItem['content'] = mood['rt_con']['content']
                except TypeError:
                    # 当一个动态只有视频
                    moodItem['content'] = mood['video'][0]['url3']

            print('Dealing with QQ: %s, moods number is: %d' % (qqnumber, self.count))
            self.insertToDB(moodItem)
            self.count += 1
            if self.count % 1000 == 0:
                self.conn.commit()

    # 供exactMoodData调用，把数据插入到sqlite数据库中
    def insertToDB(self, mood):
        sql = 'INSERT INTO moods (qq, ctime,  content, comment_count, phone, image, locate) VALUES (?, ?, ?, ?, ?, ?, ?)'
        self.cur.execute(sql, (mood['belong'], mood['create_time'], mood['content'], mood['comment_num'], mood['phone'], mood['pic'], mood['locate']))

if __name__ == '__main__':
    conn = sqlite3.connect('moods.sqlite')
    cur = conn.cursor()

    app = GetDetail(conn, cur)
    moodDict = app.makeDict()

    for dirname, fname in moodDict.items():
        for each_file in fname:
            filename = os.path.join('mood_result', dirname, each_file)
            app.exactMoodData(dirname, filename)
    else:
        conn.commit()
        cur.close()
        conn.close()
        print('Finish!')