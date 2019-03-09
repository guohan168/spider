

import time,json
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AutoSelenium(object):
    # 爬取链接,占位符为车型id
    kouBeiUrl = "https://k.autohome.com.cn/spec/%s"
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        specRes=MySqlUtils.querySpec()
        self.chexingIdSet=MySqlUtils.parseToChexingIdSet(specRes)

    def start_requests(self):
        print("===================>start")
        print(len(self.chexingIdSet))
        for chexingId in self.chexingIdSet:
            url = self.kouBeiUrl % chexingId
            self.browser.get(url)
            time.sleep(2)













import pymysql
class MySqlUtils(object):
    #获取数据库链接
    vcar_host="10.1.11.129"
    @classmethod
    def getConnection(self):
        conn = pymysql.connect(host='localhost', user='root', passwd='root', db='vcar_vcyber_com', port=3306, charset='utf8')
        return conn

    @classmethod
    def queryBrandId(self):
        #self.log("start query --------------------------------")
        queryList=list()
        try:
            conn = self.getConnection()
            cur = conn.cursor()
            sql="""
            SELECT  `vcar_pinpai`.`pinpaiID`
            FROM `vcar_vcyber_com`.`vcar_pinpai`;
            """
            cur.execute(sql)
            res=cur.fetchall()
            #for item in res:
                #print(item)
                #self.log(item)
            #返回的是列表，列表元素类型是元组[(),(),,]
            return res

        except Exception as e:
            pass
            #print(e)
            #self.log(e)
            #self.log("查询失败")
        finally:
            cur.close()
            conn.close()
        #self.log("end query ----------------------------------")


    #查询车系信息，返回元组(brandId,seriesId,seriesLink)
    @classmethod
    def querySeriesLink(self):
        sql="""
                SELECT 
                    `vcar_chexi`.`pinpaiID`,
                    `vcar_chexi`.`chexiID`,
                    `vcar_chexi`.`url`
                FROM `vcar_vcyber_com`.`vcar_chexi`;
        """
        try:
            #获取数据连接
            conn=self.getConnection()
            #获取查询游标
            cursor=conn.cursor()
            #执行查询
            cursor.execute(sql)
            #获取结果
            res=cursor.fetchall()
            #for item in res:
                #print(item)
            return res
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    @classmethod
    def insertSpecItemList(cls,itemList):
        sql="""
                INSERT INTO `vcar_vcyber_com`.`vcar_chexing`
                    (`chexingID`,
                    `pinpaiID`,
                    `chexiID`,
                    `name`,
                    `url`)
                    VALUES
                    (%s,
                    %s,
                    %s,
                    %s,
                    %s);
            """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.executemany(sql,itemList)
            # 提交
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def querySpec(cls):
        sql="""
            SELECT 
                chexingID,
                chexiID,
                pinpaiID,
                name 
            FROM vcar_vcyber_com.vcar_chexing 
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql)
            res=cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


    # 查询枚举表
    @classmethod
    def queryEnum(cls,labelCd):
        sql="""
                SELECT 
                    opitionName, optionValue
                FROM
                    vcar_vcyber_com.vcar_dic
                WHERE
                    labelCd = '%s';
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql % labelCd)
            res = cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()



    # 将车型元组集合转换为车型IDset集合
    @classmethod
    def parseToChexingIdSet(cls,res):
        chexingIdSet=set()
        for item in res:
            chexingIdSet.add(item[0])
        return chexingIdSet

    # 将车系元组集合转换成车系ID集合
    @classmethod
    def parseToSeriesIdSet(cls,res):
        seriesIdSet=set()
        for item in res:
            seriesIdSet.add(item[1])
        return seriesIdSet

    # 查询车系id集合中的车系数据
    @classmethod
    def findChexiInChexiSet(cls,seriesItems,seriesIdSet):
        waitingCrawlItems=list()
        for id in seriesIdSet:
             for item in seriesItems:
                 if id == item[1]:
                    waitingCrawlItems.append(item)
                    break
        return waitingCrawlItems;

    @classmethod
    def parseEnum(cls,res):
        enumDic=dict()
        for item in res:
            enumDic.__setitem__(item[0],item[1])
        return enumDic








import pymysql
class MySqlUtils(object):
    #获取数据库链接
    vcar_host="10.1.11.129"
    @classmethod
    def getConnection(self):
        conn = pymysql.connect(host='localhost', user='root', passwd='root', db='vcar_vcyber_com', port=3306, charset='utf8')
        return conn

    @classmethod
    def queryBrandId(self):
        #self.log("start query --------------------------------")
        queryList=list()
        try:
            conn = self.getConnection()
            cur = conn.cursor()
            sql="""
            SELECT  `vcar_pinpai`.`pinpaiID`
            FROM `vcar_vcyber_com`.`vcar_pinpai`;
            """
            cur.execute(sql)
            res=cur.fetchall()
            #for item in res:
                #print(item)
                #self.log(item)
            #返回的是列表，列表元素类型是元组[(),(),,]
            return res

        except Exception as e:
            pass
            #print(e)
            #self.log(e)
            #self.log("查询失败")
        finally:
            cur.close()
            conn.close()
        #self.log("end query ----------------------------------")


    #查询车系信息，返回元组(brandId,seriesId,seriesLink)
    @classmethod
    def querySeriesLink(self):
        sql="""
                SELECT 
                    `vcar_chexi`.`pinpaiID`,
                    `vcar_chexi`.`chexiID`,
                    `vcar_chexi`.`url`
                FROM `vcar_vcyber_com`.`vcar_chexi`;
        """
        try:
            #获取数据连接
            conn=self.getConnection()
            #获取查询游标
            cursor=conn.cursor()
            #执行查询
            cursor.execute(sql)
            #获取结果
            res=cursor.fetchall()
            #for item in res:
                #print(item)
            return res
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    @classmethod
    def insertSpecItemList(cls,itemList):
        sql="""
                INSERT INTO `vcar_vcyber_com`.`vcar_chexing`
                    (`chexingID`,
                    `pinpaiID`,
                    `chexiID`,
                    `name`,
                    `url`)
                    VALUES
                    (%s,
                    %s,
                    %s,
                    %s,
                    %s);
            """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.executemany(sql,itemList)
            # 提交
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def querySpec(cls):
        sql="""
            SELECT 
                chexingID,
                chexiID,
                pinpaiID,
                name 
            FROM vcar_vcyber_com.vcar_chexing 
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql)
            res=cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


    # 查询枚举表
    @classmethod
    def queryEnum(cls,labelCd):
        sql="""
                SELECT 
                    opitionName, optionValue
                FROM
                    vcar_vcyber_com.vcar_dic
                WHERE
                    labelCd = '%s';
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql % labelCd)
            res = cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()



    # 将车型元组集合转换为车型IDset集合
    @classmethod
    def parseToChexingIdSet(cls,res):
        chexingIdSet=set()
        for item in res:
            chexingIdSet.add(item[0])
        return chexingIdSet

    # 将车系元组集合转换成车系ID集合
    @classmethod
    def parseToSeriesIdSet(cls,res):
        seriesIdSet=set()
        for item in res:
            seriesIdSet.add(item[1])
        return seriesIdSet

    # 查询车系id集合中的车系数据
    @classmethod
    def findChexiInChexiSet(cls,seriesItems,seriesIdSet):
        waitingCrawlItems=list()
        for id in seriesIdSet:
             for item in seriesItems:
                 if id == item[1]:
                    waitingCrawlItems.append(item)
                    break
        return waitingCrawlItems;

    @classmethod
    def parseEnum(cls,res):
        enumDic=dict()
        for item in res:
            enumDic.__setitem__(item[0],item[1])
        return enumDic








import pymysql
class MySqlUtils(object):
    #获取数据库链接
    vcar_host="10.1.11.129"
    @classmethod
    def getConnection(self):
        conn = pymysql.connect(host='localhost', user='root', passwd='root', db='vcar_vcyber_com', port=3306, charset='utf8')
        return conn

    @classmethod
    def queryBrandId(self):
        #self.log("start query --------------------------------")
        queryList=list()
        try:
            conn = self.getConnection()
            cur = conn.cursor()
            sql="""
            SELECT  `vcar_pinpai`.`pinpaiID`
            FROM `vcar_vcyber_com`.`vcar_pinpai`;
            """
            cur.execute(sql)
            res=cur.fetchall()
            #for item in res:
                #print(item)
                #self.log(item)
            #返回的是列表，列表元素类型是元组[(),(),,]
            return res

        except Exception as e:
            pass
            #print(e)
            #self.log(e)
            #self.log("查询失败")
        finally:
            cur.close()
            conn.close()
        #self.log("end query ----------------------------------")


    #查询车系信息，返回元组(brandId,seriesId,seriesLink)
    @classmethod
    def querySeriesLink(self):
        sql="""
                SELECT 
                    `vcar_chexi`.`pinpaiID`,
                    `vcar_chexi`.`chexiID`,
                    `vcar_chexi`.`url`
                FROM `vcar_vcyber_com`.`vcar_chexi`;
        """
        try:
            #获取数据连接
            conn=self.getConnection()
            #获取查询游标
            cursor=conn.cursor()
            #执行查询
            cursor.execute(sql)
            #获取结果
            res=cursor.fetchall()
            #for item in res:
                #print(item)
            return res
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    @classmethod
    def insertSpecItemList(cls,itemList):
        sql="""
                INSERT INTO `vcar_vcyber_com`.`vcar_chexing`
                    (`chexingID`,
                    `pinpaiID`,
                    `chexiID`,
                    `name`,
                    `url`)
                    VALUES
                    (%s,
                    %s,
                    %s,
                    %s,
                    %s);
            """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.executemany(sql,itemList)
            # 提交
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def querySpec(cls):
        sql="""
            SELECT 
                chexingID,
                chexiID,
                pinpaiID,
                name 
            FROM vcar_vcyber_com.vcar_chexing 
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql)
            res=cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


    # 查询枚举表
    @classmethod
    def queryEnum(cls,labelCd):
        sql="""
                SELECT 
                    opitionName, optionValue
                FROM
                    vcar_vcyber_com.vcar_dic
                WHERE
                    labelCd = '%s';
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql % labelCd)
            res = cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()



    # 将车型元组集合转换为车型IDset集合
    @classmethod
    def parseToChexingIdSet(cls,res):
        chexingIdSet=set()
        for item in res:
            chexingIdSet.add(item[0])
        return chexingIdSet

    # 将车系元组集合转换成车系ID集合
    @classmethod
    def parseToSeriesIdSet(cls,res):
        seriesIdSet=set()
        for item in res:
            seriesIdSet.add(item[1])
        return seriesIdSet

    # 查询车系id集合中的车系数据
    @classmethod
    def findChexiInChexiSet(cls,seriesItems,seriesIdSet):
        waitingCrawlItems=list()
        for id in seriesIdSet:
             for item in seriesItems:
                 if id == item[1]:
                    waitingCrawlItems.append(item)
                    break
        return waitingCrawlItems;

    @classmethod
    def parseEnum(cls,res):
        enumDic=dict()
        for item in res:
            enumDic.__setitem__(item[0],item[1])
        return enumDic




se=AutoSelenium()
se.start_requests()