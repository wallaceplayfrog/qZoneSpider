import requests
from time import sleep
import util

class GetFriendsNumber(object):
    #从qq空间访问列表来获取好友信息
    def __init__(self):
        self.headers = util.headers
        self.baseUrl = util.parseFriendsUrl()
        util.checkPath('friends')
        print('开始获取好友列表，并把文件保存到 friends 文件夹')

    def getFriends(self):
        key = True
        position = 0
        while key:
            url = self.baseUrl + '&offset=' + str(position)
            referer = 'http://qzs.qq.com/qzone/v8/pages/setting/visit_v8.html'
            self.headers['Referer'] = referer

            print("\tDealing with position\t%d." % position)
            res = requests.get(url, headers=self.headers)
            html = res.text
            with open('friends/offset' + str(position) + '.json', 'w', encoding='utf-8') as f:
                f.write(html)

            # 检查朋友列表是否结束，如果是，uinlist为空
            with open('friends/offset' + str(position) + '.json', encoding='utf-8') as f2:
                con = f2.read()
            if "请先登录" in con:
                print("登录失败，请检查原因")
                key = False
                break
            if '''"uinlist":[]''' in con:
                print("好友列表获取完毕!")
                break
                key = False

            position += 50
            sleep(5)