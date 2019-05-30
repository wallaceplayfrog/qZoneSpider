import getFriends
import getMoods
import getNumber
import login

if __name__ == '__main__':
    # 登录,获取cookie，cookie过期时运行
    #mylogin = login.Login()
    #mylogin.login()

    # 先获取包含好友QQ号码的文件
    #friends = getFriends.GetFriendsNumber()
    #friends.getFriends()

    # 第二步清洗数据
    # 从这些文件里面提取出QQ号码
    # 保存到文件 qqnumber.inc
    #qqFile = getNumber.exactData()
    #qqFile.exactNumber()

    # 最后，根据每一个QQ号码去获取对应的动态
    moods = getMoods.moodsStart()
    moods.getMoodsStart()
