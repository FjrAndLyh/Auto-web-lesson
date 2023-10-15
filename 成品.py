import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import io
import requests
from PIL import Image, ImageChops

#用户信息
username = '账号'
password = '密码'
#判断播放完毕标志位   
style = '0'
#伪造用户代理
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
# Chrome浏览器
browser = webdriver.Chrome(opts)
url = r'https://changjiang.yuketang.cn/v2/web/index'#长江与课堂
#打开网站并登录,填入用户名和密码
def login(username,password):
    browser.maximize_window()
    browser.get(url)
    #点击密码登录
    browser.find_element(By.CLASS_NAME,'changeImg').click()

    browser.find_element(By.NAME,'loginname').send_keys(username)

    browser.find_element(By.NAME,'password').send_keys(password)

    browser.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[5]').click()


#driver.find_element(By.XPATH, "//*[contains(text(), '下一页')]")

#暂时不自动绕过滑块，只能手动拖动
def find_lesson():
    time.sleep(5)
    browser.switch_to.window(browser.window_handles[0])
    #我听的课
    browser.find_element(By.XPATH,"//*[contains(text(), '课程班级')]").click()
    browser.find_element(By.XPATH,"//*[contains(text(), '我听的课')]").click()
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[0])
    #这里填入课程老师的名字
    browser.find_element(By.XPATH,"//*[contains(text(), '谭来兴')]").click()
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[0])
    #成绩单
    browser.find_element(By.XPATH,"//*[contains(text(), '成绩单')]").click()
#自动播放
def auto_play(style):
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[-1])
    #这里找到了每个视频的xpath之间的联系，具体就是after那个地方每次都＋1，所以可以以这种方式自动连播，也可寻找其他规律后修改
    for i in range(1,29):
        after = str(i)
        path = '//*[@id="pane-student_school_report"]/div/div[2]/section[2]/div[2]/ul/li['+after+']/div[1]/span'
        browser.find_element(By.XPATH,path).click()
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[-1])
        while (style!='完成度：100%'):
            time.sleep(20)
            list = browser.find_element(By.XPATH,'//*[@id="app"]/div[2]/div/div[2]/div/div[1]/div/section[1]/div[2]/div/div/span')
            style = list.text
            print(style)
        style = '0'
        time.sleep(2)
        browser.close()
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[0])




login(username,password)
find_lesson()
auto_play(style)

down = input("输入1关闭")
if down == 1:
    browser.close()
