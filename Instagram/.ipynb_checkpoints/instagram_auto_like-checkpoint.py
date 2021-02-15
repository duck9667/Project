import time
import datetime
import random
from selenium import webdriver
from slacker import Slacker
from urllib.parse import quote
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

# ======== 1. Setting Options =======
# slack_token : 작업이 진행될 때 중간 중간 슬랙에 메세지 발송
slack_token= 'xoxp-1602605362180-1589664665606-1583851108199-67d4cdd095c1819a245d30d01c080e4e'
slack= Slacker(slack_token)

# Chrome을 안 띄우고 수행하고 싶으면 아래 주석을 해제(리눅스 서버에서 작업시 headless 추천, 디버깅시는 headless 주석처리)
# options.add_argument("headless")

# Chrome 설정 : 진짜 유저가 작업하는 것처럼 보이도록 설정
options = webdriver.ChromeOptions()
options.add_argument("window-size=1920x1080")
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 \
                      (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR")

# ======= 2. Setting id, password, hashtag ======
id = 'duck9667@kakao.com' # 'kjh9667@gmail.com'
password = 'dhfl6395!@'
hash_tags = ['자바', '오리']
post_num = 10


class InstaJob:
    @classmethod
    def run(cls):        
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        browser = webdriver.Chrome(r'C:\Users\82109\Desktop\곽종현\03 Github\duck9967\ETC\chromedriver.exe', options=options)
        browser.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
        browser.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
        browser.execute_script(
            "const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = \
            function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) \
            {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")

        browser.get('https://instagram.com/')
        time.sleep(2)

        login_id = browser.find_element_by_name('username')
        login_id.send_keys(id)
        time.sleep(2)

        login_id = browser.find_element_by_name('password')
        login_id.send_keys(password)
        login_id.submit()

        text = '로그인 완료했습니다.'
        print(text)    
        slack.chat.post_message('#일반', text)
        
        try : 
            for hash_tag in hash_tags :
                text = '"#' + hash_tag + '"' + " 좋아요 작업을 시작합니다."
                print(text)
                slack.chat.post_message('#일반', text=text)
                time.sleep(2)

                browser.get("https://www.instagram.com/explore/tags/" + quote(hash_tag))
                time.sleep(5)

                feed = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a')
                feed.send_keys(Keys.ENTER)

                for i in range(post_num) : 
                    time.sleep(1)
                    like_list = browser.find_elements_by_xpath('//article//section/span/button')
                    like_list[0].click()

                    nextFeed = browser.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.EfHg9 > div > div > a._65Bje.coreSpriteRightPaginationArrow')
                    nextFeed.click()

                text = '"#' + hash_tag + '"' + " 좋아요 작업을 종료합니다."
                print(text)
                slack.chat.post_message('#일반', text=text)
        
        except Exception as e: 
            text = "'NosuchError' 에러가 발생했습니다. @오리에게 문의해주세요."
            print(e)
            slack.chat.post_message('#일반', text=text)
            raise

        browser.quit()
        
if __name__ == '__main__':
    InstaJob.run()