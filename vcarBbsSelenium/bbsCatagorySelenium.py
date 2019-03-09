

import time,json,re,random,datetime
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy import Selector
class BbsCatagorySelenium(object):
    # 论坛主页网址
    bbsLink="https://club.autohome.com.cn"
    # 保存论坛定义主表表集合
    insertBbsList=list()
    # 更新论坛表集合
    updateBbsList=list()

    # 统计保存个数
    insertCount=0

    # 统计更新个数
    updateCount=0



    def __init__(self):
        # 初始化selenium
        self.browser=webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        # 已存存在于数据库中的论坛主键id集合
        bbsHeadRes=MySqlUtils.query(MySqlUtils.sql_query_bbs)
        self.existBbsIdSet=MySqlUtils.parseToSet(bbsHeadRes,0)





    # 爬虫入口
    def start_request(self):
        # 请求链接
        self.requestLink(self.bbsLink)
        # 依次点击字母A、B、C、、、、
        elements=self.browser.find_elements(By.CSS_SELECTOR,"#_c a")
        for element in elements:
            className=element.get_attribute("class")

            if "btn btn-mini" == className:
                # 获取字母
                letter=element.text
                print()
                print("-------------------------letter:%s--------------------" % letter)
                # 点击字母元素
                element.click()
                time.sleep(1)

                # 取出page_source
                page_source = self.browser.page_source
                # 转selector取值
                response = Selector(text=page_source)
                # 解析
                self.parse(response)

        # 请求完成，关闭浏览器
        self.browser.close()







    def requestLink(self, url):
        success=True
        wait=None
        try:
            self.browser.get(url)
            wait = WebDriverWait(self.browser, 10)
            wait.until(EC.presence_of_element_located((By.ID, '_c')))
            time.sleep(0.1)  # 若不加一个会发生页面没有完全渲染
        except Exception as e:
            print(e)
            success=False
        return success


    # 解析
    def parse(self,response):
        dataDiv=response.css(".forum-brand-box")
        brands=dataDiv.css("p ::text")
        seriesDataList=dataDiv.css("ul")
        for i,brand in enumerate(brands):
            brandName=brand.extract()
            print("brandName:%s" % brandName)
            seriesData=seriesDataList[i].css("a")
            for series in seriesData:
                bbsName=series.css("::text").extract_first().strip()
                bbsUrl=series.css("::attr(href)").extract_first().strip()
                chexiId=re.search(r'\d+',bbsUrl).group()
                bbsId=bbsUrl[bbsUrl.rfind("/")+1:bbsUrl.rfind(".")]
                print("bbsName:%s  ,bbsUrl:%s ,chexiId:%s" % (bbsName,bbsUrl,chexiId))
                # 如果数据库中不存在则保存，否则更新
                if bbsId not in self.existBbsIdSet:
                    insertParams=(bbsId,bbsUrl.strip(),bbsName.strip())
                    self.insertBbsList.append(insertParams)
                    self.insertCount += 1
                else:
                    updateDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    updateParams=(bbsName,updateDate,bbsId)
                    self.updateBbsList.append(updateParams)
                    self.updateCount += 1

        # 保存到数据库
        self.save()



    # 保存到数据库
    def save(self):
        if len(self.insertBbsList) > 0:
            MySqlUtils.updateList(sql=MySqlUtils.sql_insert_bbs,paramsList=self.insertBbsList)
            self.insertBbsList.clear()
            print("insertCount:%s" % self.insertCount)

        if len(self.updateBbsList) > 0:
            MySqlUtils.updateList(sql=MySqlUtils.sql_update_bbs,paramsList=self.updateBbsList)
            self.updateBbsList.clear()
            print("updateCount:%s" % self.updateCount)




import pymysql
class MySqlUtils(object):
    #获取数据库链接
    vcar_host="10.1.11.129"


    # 查询用户
    sql_query_user="""
                        SELECT 
                            sid
                        FROM
                            vcar_vcyber_com.vcar_qczj_user;
    """
    # 更新用户
    sql_update_user="""
                        UPDATE `vcar_vcyber_com`.`vcar_qczj_user`
                        SET
                            `userName` = %s,
                            `headImg` = %s,
                            `updateTime` = %s
                        WHERE `sid` = %s;
    """
    # 插入用户
    sql_insert_user="""
                        INSERT INTO `vcar_vcyber_com`.`vcar_qczj_user`
                        (`sid`,
                        `userName`,
                        `homepageUrl`,
                        `headImg`,
                        `city`,
                        `county`)
                        VALUES
                        (%s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s);
    """

    # 查询论坛主表
    sql_query_bbs="""
                        SELECT 
                            sid
                        FROM
                            vcar_vcyber_com.vcar_qczj_bbs;
    """
    # 插入论坛主表
    sql_insert_bbs="""
                        INSERT INTO `vcar_vcyber_com`.`vcar_qczj_bbs`
                            (`sid`,
                            `bbsUrl`,
                            `bbsName`)
                            VALUES(
                            %s,
                            %s,
                            %s);
    """
    # 更新论坛表
    sql_update_bbs="""
                        UPDATE `vcar_vcyber_com`.`vcar_qczj_bbs`
                        SET
                            `bbsName` =%s,
                            `updateTime` = %s
                        WHERE `sid` = %s;
    """



    @classmethod
    def getConnection(self):
        conn = pymysql.connect(host='localhost', user='root', passwd='root', db='vcar_vcyber_com', port=3306, charset='utf8')
        return conn


    @classmethod
    def query(cls,sql):
        try:
            # 获取链接
            conn = cls.getConnection()
            cursor = conn.cursor()
            cursor.execute(sql)
            res=cursor.fetchall()
            #for item in res:
                #print(item)
                #self.log(item)
            #返回的是列表，列表元素类型是元组[(),(),,]
            return res
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    # 批量更新或保存
    @classmethod
    def updateList(cls,sql,paramsList):
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.executemany(sql, paramsList)
            # 提交
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    # 只更新一个
    @classmethod
    def updateOne(cls,sql,params):
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql, params)
            # 提交
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    # 将查询结果解析成id集合
    @classmethod
    def parseToSet(cls,res,index):
        idSet=set()
        for item in res:
            idSet.add(item[index])
        return idSet
    # 解析成字典
    @classmethod
    def parseToDict(cls,res,keyIndex,valueIndex):
        d=dict()
        for item in res:
            d.__setitem__(item[keyIndex],item[valueIndex])
        return d

bbsC=BbsCatagorySelenium()
bbsC.start_request()