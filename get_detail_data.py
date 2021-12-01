from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time,os,config

class Get_detail_data():
    def __init__(self):
        # self.domain=domain
        # self.keyword=keyword
        # self.video_num=video_num
        self.driver=webdriver.Chrome()
    def __driver_slide(self):
        body = self.driver.find_element_by_tag_name("body")
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.6)
        body.send_keys(Keys.PAGE_DOWN)
    def get_youtube_detail(self,keyword,video_num:int):
        res=[]
        self.driver.get('https://www.youtube.com/results?search_query={}&sp=CAASBBABGAE%253D'.format(keyword))
        for slide_count in range(0,100):#循环下拉
            self.__driver_slide()
            time.sleep(1)
            detail_url_list = self.driver.find_elements_by_xpath("//div[@id='dismissible']//a[@id='thumbnail']")
            getting_num=len(detail_url_list)
            print(f'下拉第{slide_count}次,获取到关键字:{keyword},共{getting_num}个视频!!')
            if getting_num>video_num+4:
                self.__driver_slide()
                break
        detail_url_list = self.driver.find_elements_by_xpath("//div[@id='dismissible']//a[@id='video-title']")[0:video_num]
        detail_img_list = self.driver.find_elements_by_xpath("//div[@id='dismissible']//a[@id='thumbnail']//*[@id='img']")[0:video_num]
        for count in range(0,len(detail_url_list)):
            data={}
            data['url']=detail_url_list[count].get_attribute('href')
            data['title']=detail_url_list[count].get_attribute('title')
            data['img_src']=detail_img_list[count].get_attribute('src')
            data['keyword']=keyword
            data['source'] = data['url'].split('=')[1]
            if data not in res:
                res.append(data)
        return res

    def run(self,domain,keyword,video_num):
        if domain=='youtube':
            res=self.get_youtube_detail(keyword,video_num)
        else:
            raise TypeError('domain未匹配')
        self.driver.close()
        return res

if __name__ == '__main__':
    get=Get_detail_data()
    print(get.run('youtube', 'Cricket+team',50))