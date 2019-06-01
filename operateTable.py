import sqlite3
import sys

class OperateTable(object):

    def __init__(self):
        self.conn = sqlite3.connect('moods.sqlite')
        self.cur = self.conn.cursor()

    def createTable(self):
        sql = '''CREATE TABLE moods (
                 id integer primary key Autoincrement not null,
                 qq int not null,
                 content text null,
                 comment_count int not null,
                 ctime int not null,
                 phone text null,
                 image text null,
                 locate text null)'''
        self.cur.execute(sql)

    def dropTable(self):
        self.cur.execute('drop table moods')

if __name__ == '__main__':
    app = OperateTable()
    argv = sys.argv[1]
    
    if argv == 'createTable':
        app.createTable()
    elif argv == 'dropTable':
        app.dropTable()
    else:
        print("输入参数必须为createTable或dropTable其中之一")
        raise ValueError
