'''获取cookie
   userinfo
'''

from selenium import webdriver
import json
import time

class Login(object):
    def __init__(self):
        self.qq, self.password = self.getUsernamePassword() 

    def getUsernamePassword(self):
        infopath = '/home/yanglin/桌面/spider/userinfo.json'
        try:    
            with open(infopath, 'r', encoding = 'utf-8') as r:
                userinfo = json.load(r)
            return userinfo["username"], userinfo["password"]
        except:
            print("Error: File Not Found==============")
            print("请检查配置文件是否正确配置!!!!")
            print("Please check config file")
            print("Path:", infopath)
            exit(1)

    def login(self):
        driver = webdriver.Chrome()
        driver.maximize_window() #窗口最大化
        driver.get('https://user.qzone.qq.com/{}/311'.format(self.qq))  #URL
        driver.implicitly_wait(10)  # 隐示等待，充分加载好网址

        driver.find_element_by_id('login_div')
        driver.switch_to_frame('login_frame') #切到输入账号密码的frame
        driver.find_element_by_id('switcher_plogin').click()#点击‘账号密码登录’
        driver.find_element_by_id('u').clear() #清空账号栏
        driver.find_element_by_id('u').send_keys('{}'.format(self.qq))#输入账号
        driver.find_element_by_id('p').clear()#清空密码栏
        driver.find_element_by_id('p').send_keys('{}'.format(self.password))#输入密码
        driver.find_element_by_id('login_button').click()#点击‘登录’
        driver.switch_to_default_content()   #跳出当前的frame

        driver.implicitly_wait(10)
        time.sleep(10)
        with open(r'cookie_file', 'w+') as f:#这里是将得到的cookie进行保存，这样就不用每次启动程序都要登录
            for cookie in driver.get_cookies():
                print(cookie)
                f.write(cookie['name']+'='+cookie['value']+';')
        f.close()
        driver.quit()
        driver.close()

mylogin = Login()
mylogin.login()