

import scrapy,pymysql,re,json,random,datetime
from ..pipelines import CiYunPipeline
from ..mySqlUtils import MySqlUtils

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, re,timeit,random,traceback
from scrapy import Selector

class CiYunSpider(scrapy.Spider):
    name = "ciYunSpider"
    # 词云爬取链接,第一个占位符为车型id，第二个为评价细分类别：1 外观 2 内饰 3 舒适性 4 空间 5 动力 6 操控 7 油耗 8 性价比
    ciYunLink = "https://k.autohome.com.cn/spec/%s/ge%s"
    browser = webdriver.Chrome()

    def start_requests(self):

        for item in MySqlUtils.querySpec():
            chexingId=item[0]
            chexiId=item[1]
            # 分类请求词云
            # for i in ['1','2','3','4','5','6','7','8']:
            #     self.browser.get(self.ciYunLink % (chexingId,i))
            #     # wait = WebDriverWait(self.browser, 10)
            #     # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tbcs')))
            #     time.sleep(2)  # 若不加一个会发生页面没有完全渲染
            #     find=True
            #     ele=None
            #     try:
            #         ele=self.browser.find_element_by_css_selector(".geetest_radar_tip")
            #     except Exception as e:
            #         find=False
            #
            #     if find:
            #         ele.click()

        self.browser.get("http://safety.autohome.com.cn/userverify/index?locnum=104092&backurl=//k.autohome.com.cn%2Fspec%2F1000004%2Fge5")
        # wait = WebDriverWait(self.browser, 10)
        # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tbcs')))
        time.sleep(2)  # 若不加一个会发生页面没有完全渲染
        find=True
        ele=None
        try:
            ele=self.browser.find_element_by_css_selector(".geetest_radar_tip")
        except Exception as e:
            find=False

        if find:
            ele.click()

                # request=scrapy.Request(url=self.ciYunLink % (chexingId,i),callback=self.parse,dont_filter=True)
                # request.meta['chexiId']=chexiId
                # yield request



    def parse(self, response):
        print("======================>parse")
        data=response.css(".revision-impress a::text")
        if data:
            for item in data:
                self.log(item.extract())


        pass



