import Friends
import Moods
import Number
import login

if __name__ == '__main__':
    # 登录,获取cookie，cookie过期时运行
    #mylogin = login.Login()
    #mylogin.login()

    # 获取包含好友QQ号码的文件
    friends = Friends.GetFriendsNumber()
    friends.getFriends()

    # 清洗数据
    # 提取QQ号码
    qqFile = Number.exactData()
    qqFile.exactNumber()

    # 获取动态
    #moods = Moods.moodsStart()
    #moods.getMoodsStart()
