'''dropped
'''

from selenium import webdriver
import os
from lxml import etree
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt  
import jieba  
import datetime
from copy import deepcopy
import json

class BaseSpider(object):
    def __init__(self, username = '', nickname = '', targetqq = '', title = [], comment = []):
        self.begin_time = datetime.datetime.now()
        self.username, self.password, self.file_name_head = self.get_username_password()
        self.nickname = nickname
        self.targetqq = targetqq

        self.page = 0
        self.comment = comment
        self.title = title
        self.nodes = []
        self.data = []

        self.file = '/home/yanglin/桌面/{}.txt'.format(self.targetqq)
        self.font_path='/home/yanglin/桌面/SIMYOU.TTF'

    def get_username_password(self):
        infopath = '/home/yanglin/桌面/spider/userinfo.json'
        try:    
            with open(infopath, 'r', encoding = 'utf-8') as r:
                userinfo = json.load(r)
            return userinfo["username"], userinfo["password"], userinfo["file_name_head"]
        except:
            print("Error: File Not Found==============")
            print("请检查配置文件是否正确配置!!!!")
            print("Please check config file")
            print("Path:", infopath)
            exit(1)

    def get_wordcloud(self):
        f = open(self.file, 'r', encoding='UTF-8').read()
        # 生成词云
        cut_text = " ".join(jieba.cut(f))
        wordcloud = WordCloud(
            # 设置字体or乱码
            self.font_path,
            # 设置背景，宽高
            background_color="white", width=2000, height=1380).generate(cut_text)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    def get_qzone(self):
        driver = webdriver.Chrome()
        driver.maximize_window() #窗口最大化
        driver.get('https://user.qzone.qq.com/{}/311'.format(self.targetqq))  #URL
        driver.implicitly_wait(10)  # 隐示等待，充分加载好网址

        driver.find_element_by_id('login_div')
        driver.switch_to_frame('login_frame') #切到输入账号密码的frame
        driver.find_element_by_id('switcher_plogin').click()#点击‘账号密码登录’
        driver.find_element_by_id('u').clear() #清空账号栏
        driver.find_element_by_id('u').send_keys('{}'.format(self.username))#输入账号
        driver.find_element_by_id('p').clear()#清空密码栏
        driver.find_element_by_id('p').send_keys('{}'.format(self.password))#输入密码
        driver.find_element_by_id('login_button').click()#点击‘登录’
        driver.switch_to_default_content()   #跳出当前的frame

        driver.implicitly_wait(10)
        time.sleep(3)

        try:
            driver.find_element_by_id('QM_OwnerInfo_Icon')#判断是否QQ空间加了权限
            b = True
        except:
            b = False

        if b==True:
            self.page = 1

            try:
                while self.page:
                    ##下拉之前回到顶部
                    driver.find_element_by_id('goto_top_btn').click()
                    for j in range(1, 5):                        
                        driver.execute_script("window.scrollBy(0,5000)")
                        time.sleep(2)
                    
                    driver.switch_to_frame('app_canvas_frame')#切入说说frame
                    #if self.page > 1:
                        #driver.find_elements_by_class_name('comment_btn').click()
                        #driver.find_element_by_xpath('//li/div/div/div/a[2]').click()#点击显示评论
                    selector = etree.HTML(driver.page_source)
                    
                    #从上到下依次为说说发表时间，说说内容，主回复人昵称，主回复内容。从回复昵称，从回复内容。
                    self.data = selector.xpath('''
                        //div[@class="info"]/span/a/text() |
                        //li/div/div/pre/text() |
                        //li/div/div/div/a[@class="nickname"]/text() |
                        //li/div/div/div[@class="comments_content"]/span[last()]/text() |
                        //li/div/div/a[@class="nickname"]/text() |
                        //li/div/div[@class="comments_content"]/span[last()]/text()
                    ''')
                    print(self.data)

                    #self.title = selector.xpath('//li/div/div/pre/text()') #获取title集合
                    #print(self.title)
                    #person = selector.xpath('//li/div/div/div/a[@class="nickname"]/text()')
                    #print(person)
                    #self.comment = selector.xpath('''
                    #    //li/div/div/div/a[@class="nickname"]/text() | 
                    #    //li/div/div/div[@class="comments_content"]/span[last()]/text() | 
                    #    //li/div/div/a[@class="nickname"]/text() | 
                    #    //li/div/div[@class="comments_content"]/span[last()]/text()
                    #    ''')
                    #print(self.comment)

                    #for i in title:
                        #if not os.path.exists(self.file):
                            #print('创建TXT成功')

                        #with open(self.file, 'a+') as f:
                            #f.write(i + '\n\n')
                            #f.close()
                            
                    self.page = self.page + 1
                    driver.find_element_by_link_text(u'下一页').click()  #点击下一页
                    driver.switch_to.default_content()    #跳出当前frame
                    time.sleep(3)
                driver.quit()
            except Exception as e:
                #没有判断什么时候为最后一页，当爬取到最后一页，默认点击下一页，会出现异常，直接在这认为它是爬到末尾了，还是有待优化
                self.page -= 1
                print("爬取完成，爬到的最后页数为" + str(self.page))
                #self.get_wordcloud()
                driver.quit()
                driver.close()

    def result_report(self):
        print("#######################")
        print('爬取用户:', self.targetqq)
        print('总耗时:', (datetime.datetime.now() - self.begin_time).seconds / 60, '分钟')
        print('QQ空间动态数据数量:')
        print('最终失败的数据量:')
        print('--------------')
        print('动态:')
        print('评论好友列表:')
        print('--------------')
        print("########################")

if __name__ == '__main__':
    test = BaseSpider(targetqq='2425779559')
    test.get_qzone()