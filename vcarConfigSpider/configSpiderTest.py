from Python.spider_vcar_vcyber_com.vcarConfigSpider.mySqlUtils import MySqlUtils
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json,re


class ConfigSpider(object):
    https = "https:%s"
    host = "https://car.autohome.com.cn%s"
    configLinkModel = "https://car.autohome.com.cn/config/spec/%s.html"

    keyLinkDic=dict()
    configDic=dict()
    shuxingTypeDic=dict() #{"name":"id"}
    shuxingDic=dict()     #{"id":"name"}
    #伪元素键值对
    spanValueDic=dict()
    browser=webdriver.Chrome()





    def process(self):
        # 初始化shuxingTypeDic shuxingDic
        self.shuxingTypeDic=MySqlUtils.queryShuxingType()
        self.shuxingDic=MySqlUtils.queryShuxing()

        # 1、查询车型表，获取车型配置链接
        specList = MySqlUtils.querySpecLink()
        for item in specList:
            # 清空上一次的spanValue数据
            self.spanValueDic.clear()

            # 2、摸拟浏览器请求获取页面
            configUrl=self.configLinkModel % item[0]
            self.requestConfigLink(configUrl)
            page_source=self.browser.page_source

            # 解析伪元素
            self.spanValueDic=self.parseSpanValue()

            # 3、解析keyLink
            keyLinkDic=self.parseKeyLink()
            #print(keyLinkDic)

            # 4、解析config
            #configDic=self.parseConfig(page_source)

            # 5、更新属性

            # 6、更新配置
        pass


    def requestConfigLink(self,configUrl):

        self.browser.get(configUrl)
        wait=WebDriverWait(self.browser,10)
        wait.until(EC.presence_of_element_located((By.ID,'tab_0')))
        return self.browser


    # 解析keyLink
    def parseKeyLink(self):
        #将&lt;&gt;反转义
        page_source=self.browser.page_source
        sub_js=page_source[page_source.find("var keyLink = {") + 14:page_source.find("</script>",page_source.find("var keyLink = {"))]
        #print(sub_js)
        sub_js=re.sub(r'&lt;','<',sub_js)
        sub_js=re.sub(r'&gt;','>',sub_js)
        #print(sub_js)

        # 1、提取keyLink json对象字符串
        # startIndex = self.browser.page_source.find("var keyLink = {") + 14
        # subStr = page_source[startIndex:]
        # #(subStr)
        keyLinkStr = sub_js[0:sub_js.find(";")]
        print(keyLinkStr)
        keyLink = json.loads(keyLinkStr)
        #print(keyLink["result"]["items"][0]["name"])
        insertFlag=False
        for item in keyLink["result"]["items"]:
            keys = re.findall(r'\'.{10,20}\'', item['name'])
            id = item['id']
            name = item['name']
            #将name中的伪元素替换成实际的值
            for index, key in enumerate(keys):
                key=key.strip("'")
                spanValue = ""
                print(key)
                #首先从spanValueDic中取值，若取不到则证明还没赋值，则执行js取值后再赋值
                if self.spanValueDic.get(key):
                    spanValue=self.spanValueDic.get(key)
                else:
                    #执行js取值后再赋值
                    js = "return window.getComputedStyle(document.getElementsByClassName('" + key + "')[0], 'before').getPropertyValue('content')"
                    spanValue=self.browser.execute_script(js)
                    self.spanValueDic.setdefault(key,spanValue)

                if self.spanValueDic.get(key) :
                    value=self.spanValueDic.get(key)
                name = re.sub(r'<span class=.{8,20}></span>', spanValue, name)
            #print(name)


            # print(re.findall(r'\'.{10,20}\'',item['name']))
            # print(item["id"],item["name"])

        # 解析属性id


        # 解析属性名

        # shuxingDic中是否存在该id，如果不存在则做插入操作

        pass

    # 解析config
    def parseConfig(self,page_source):
        # 清空记录

        # 解析id

        # 解析value

        # 组装configParams

        # 返回configParams
        
        pass


    # 解析伪元素的值
    def parseSpanValue(self):
        elements=self.browser.find_elements(By.CSS_SELECTOR, ".tbcs")
        for index,table in enumerate(elements):
            #第一table为产商指导价，不需要爬取
            #从第二个table开始爬取
            if index == 1:
                #解析伪元素

                pass









        return self.spanValueDic






sc=ConfigSpider()
sc.process()



