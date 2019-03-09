

import time,json,re,random,datetime
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy import Selector
from fontTools.ttLib import TTFont

class  CiYunSpider(object):
    # 词云爬取网址链接
    ciYunLink="https://k.autohome.com.cn/spec/%s/ge%s"
    # 全局计数器,统计所有爬取，不论请求是否成功
    count=0
    # 车型爬取成功计数器,爬取不成功即请求超时的不计数
    specCount=0
    # 请求计数器
    requestCount=0
    # 用于记录新增爬取到的数据
    wordsInsertList=list()
    # 用于记录更新爬取的数据
    wordsUpdateList=list()

    # 断点功能：已爬取的车型id
    crawledIdSet=set()
    # 断点功能：等待爬取的车型id
    waitingCrawlIdSet=set()



    #初始化爬虫
    def __init__(self):
        # 初始化selenium
        self.browser=webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        # 查询所有车型id
        specList=MySqlUtils.query(MySqlUtils.sql_query_spec)
        self.chexingIdSet=MySqlUtils.parseToSet(specList,0)
        # 从字典表查询词云所属口碑分类
        koubeiTypeRes=MySqlUtils.query(MySqlUtils.sql_query_dict % 'qczj_koubei_type')
        print("koubeiType:")
        print(koubeiTypeRes)
        self.koubeiDict=MySqlUtils.parseToDict(koubeiTypeRes,0,1)
        # 查询词云表中已爬取的车型,用于有则更新，无则插入
        savedCiyunRes=MySqlUtils.query(MySqlUtils.sql_query_crawled_ciyun)
        self.saveIdSet=MySqlUtils.parseToSet(savedCiyunRes,0)

        # 初始化断点
        Point.init()
        # 切入断点
        self.waitingCrawlIdSet=Point.cutInto(self.chexingIdSet)





    # 爬虫入口
    def start(self):
        for chexingId in self.chexingIdSet:
            self.count += 1
            self.specCount += 1
            self.crawledIdSet.add(chexingId)
            success=True
            for koubeiType in ['1','2','3','4','5','6','7','8']:
                self.requestCount +=1
                koubeiUrl=self.ciYunLink % (chexingId,koubeiType)
                # 请求,如果没有请求成功，则跳过本次请求并不做记录
                if not self.request(koubeiUrl):
                    self.specCount -= 1;
                    self.crawledIdSet.remove(chexingId)
                    print("请求超时！")
                    break

                # 取出page_source
                page_source = self.browser.page_source
                # 转selector取值
                response = Selector(text=page_source)
                self.parse(response, chexingId, koubeiType)

        # 全部爬取结束，保存已爬车型ID，若没有出现超时等异常，则生成结束标识文件，即over.txt文件
        Point.savePoint(self.crawledIdSet)
        if self.specCount >= self.waitingCrawlIdSet:
            Point.complete()





    # 解析请求结果
    def parse(self,response,chexingId,koubeiType):
        wordLinks=response.css(".revision-impress a")
        if wordLinks:
            for index,link in enumerate(wordLinks):
                if index == 0:
                    continue
                # 提取词语,例如：空间大(10)
                wordAndCount=link.xpath("string(.)").extract_first()
                word=wordAndCount[0:wordAndCount.rfind("(")]
                # 提取参与评价人数
                print("word:%s" % wordAndCount)
                peopleCount=re.search(r'\d+',wordAndCount).group()
                # 提取样式类，用于判断语义情感
                className=link.css("::attr(class)").extract_first()
                className=className.strip()
                # 判断语义情感,0为负面，1为正面
                affectiveType = 1
                if className == 'dust':
                    affectiveType = 0

                # 判断是否已爬取过
                if chexingId in self.saveIdSet:
                    updateDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.wordsUpdateList.append((koubeiType,word,peopleCount,affectiveType,updateDate,chexingId,koubeiType))
                    print((koubeiType,word,peopleCount,affectiveType,updateDate,chexingId,koubeiType))
                else:
                    # 生成sid
                    sid=self.generateSid(chexingId,koubeiType)
                    self.wordsInsertList.append((sid,chexingId,koubeiType,word,peopleCount,affectiveType))
                    print((sid,chexingId,koubeiType,word,peopleCount,affectiveType))

            # 如果只剩下最后50个车型待爬取，则每爬一次保存一次，否则批量保存
            if self.count > len(self.waitingCrawlIdSet) - 50:
                self.updateCiyun()
            else:
                if len(self.wordsInsertList) > 100 or len(self.wordsUpdateList) > 100:
                    self.updateCiyun()



    # 发起请求
    def request(self,url):
        try:
            self.browser.get(url)
            wait = WebDriverWait(self.browser, 5)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.filter-text')))
            time.sleep(0.1)  # 若不加一个会发生页面没有完全渲染
            return True
        except Exception as e:
            print(e)
            return False


    def generateSid(self,chexingId,koubeiType):
        return chexingId + "_" + koubeiType + "_" + str(random.randint(100000,999999))

    def updateCiyun(self):
        if len(self.wordsInsertList) > 0:
            insertListCopy=self.wordsInsertList.copy()
            self.wordsInsertList.clear()
            MySqlUtils.updateList(MySqlUtils.sql_insert_ciyun,insertListCopy)
        if len(self.wordsUpdateList) > 0:
            updateListCopy=self.wordsUpdateList.copy()
            self.wordsUpdateList.clear()
            MySqlUtils.updateList(MySqlUtils.sql_update_ciyun,updateListCopy)

        Point.savePointFromSet(self.crawledIdSet.copy())
        self.crawledIdSet.clear()

        print(">>>>>>>>>>>>>>>>>>>save:%s" % self.specCount)




import pymysql
class MySqlUtils(object):
    # 获取数据库链接
    vcar_host = "10.1.11.129"
    # 查询车型sql
    sql_query_spec="""
                     SELECT 
                            chexingID,
                            chexiID,
                            pinpaiID,
                            name 
                     FROM vcar_vcyber_com.vcar_chexing 
    """

    # 查询字典表
    sql_query_dict="""
                        SELECT 
                            t.optionName, t.optionValue
                        FROM
                            vcar_vcyber_com.vcar_dic t
                        WHERE
                            t.labelCd = '%s'
    """

    # 查询词云表中已爬取的车型
    sql_query_crawled_ciyun="""
                        SELECT DISTINCT
                            (t.chexingId) AS chexingId
                        FROM
                            vcar_vcyber_com.vcar_qczj_ciyun t
    """

    # 插入词云
    sql_insert_ciyun="""
                        INSERT INTO `vcar_vcyber_com`.`vcar_qczj_ciyun`
                            (`sid`,
                            `chexingID`,
                            `ciYunType`,
                            `word`,
                            `peopleCount`,
                            `affectiveType`)
                            VALUES
                            (%s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s);
    """

    # 更新词云
    sql_update_ciyun="""
                        UPDATE `vcar_vcyber_com`.`vcar_qczj_ciyun`
                        SET
                        `ciYunType` =%s,
                        `word` = %s,
                        `peopleCount` = %s,
                        `affectiveType` = %s,
                        `updateTime` = %s
                        WHERE `chexingID`=%s and `ciYunType`=%s;
    """

    @classmethod
    def getConnection(self):
        conn = pymysql.connect(host='localhost', user='root', passwd='root', db='vcar_vcyber_com', port=3306,
                               charset='utf8')
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

    @classmethod
    def parseToDict(cls,res,keyIndex,valueIndex):
        d=dict()
        for item in res:
            d.__setitem__(item[keyIndex],item[valueIndex])
        return d



import os,sys

# 断点管理类
class Point(object):
    # 正常爬取结束标识文件
    overFilePath=None
    # 断点记录文件
    pointFilePath=None

    @classmethod
    def init(cls):
        # 获取当前目录
        path = os.path.abspath(__file__)
        path = path[0:path.rfind("/")]
        # 获取当前目录下所有文件  (('/Users/guohan/Documents/pworkspace/VCar/Python/spider_vcar_vcyber_com/vcarDetailSpider/vcarDetailSpider', ['__pycache__', 'spiders', 'temp'], ['__init__.py', 'items.py', 'middlewares.py', 'mySqlUtils.py', 'pipelines.py', 'settings.py']), ('/Users/guohan/Documents/pworkspace/VCar/Python/spider_vcar_vcyber_com/vcarDetailSpider/vcarDetailSpider/__pycache__', [], ['__init__.cpython-36.pyc', 'items.cpython-36.pyc', 'mySqlUtils.cpython-36.pyc', 'pipelines.cpython-36.pyc', 'settings.cpython-36.pyc']), ('/Users/guohan/Documents/pworkspace/VCar/Python/spider_vcar_vcyber_com/vcarDetailSpider/vcarDetailSpider/spiders', ['__pycache__'], ['__init__.py', 'detailSpider.py']), ('/Users/guohan/Documents/pworkspace/VCar/Python/spider_vcar_vcyber_com/vcarDetailSpider/vcarDetailSpider/spiders/__pycache__', [], ['__init__.cpython-36.pyc', 'detailSpider.cpython-36.pyc']), ('/Users/guohan/Documents/pworkspace/VCar/Python/spider_vcar_vcyber_com/vcarDetailSpider/vcarDetailSpider/temp', [], ['1.txt']))
        tt = tuple(os.walk(path))
        # 获取当前目录
        currentDir = tt[0][0]
        # 系统文件分隔符
        sep = os.sep
        # 拼接目的文件
        Point.overFilePath = currentDir + sep + "temp" + sep + "over.txt"
        Point.pointFilePath = currentDir + sep + "temp" + sep + "point.txt"


    # 切入断点，返回待爬集合
    @classmethod
    def cutInto(cls,total):
        print("--------------------cutInto--------------")

        # 定义最终要爬取的数据集
        waitingCrawlIdSet=None
        # 判断当前目录中是否存在over.text文件
        hasOverFile = os.path.exists(Point.overFilePath)
        # 如果存在结束标识文件则证明上一次完整爬取，删除标识文件和断点文件
        if hasOverFile:
            print(Point.overFilePath)
            os.remove(Point.overFilePath)
            # 清空断点文件的内容
            f = open(Point.pointFilePath, "w", encoding="utf-8")
            f.write("")
            f.flush()
            f.close()
            del f
            # 待爬数据就是查询出的全部
            waitingCrawlIdSet = total
        else:
            # 读取断点文件
            pointFile = open(Point.pointFilePath, "r+", encoding="utf-8")
            lines = pointFile.read()
            # 如果行末尾存在逗号，则消除逗号
            if len(lines) - 1 == lines.rfind(","):
                lines = lines[0:lines.rfind(",")]
            # 提取已爬取的车型id，封装成set集合
            crawledIdSet = set(lines.split(","))
            # 用全部爬取id集减去已爬取的的id集得出待爬取的id集
            waitingCrawlIdSet = total - crawledIdSet
            # print(len(DetailPipeline.waitingCrawlIdSet))
            pointFile.close()
            del pointFile
            print("总共需要爬取%s,上次已爬取%s,本次需爬取%s" % (len(total),len(total)-len(waitingCrawlIdSet),len(waitingCrawlIdSet)))
        return waitingCrawlIdSet

    # 记录断点
    @classmethod
    def savePoint(self,data):
        f = open(self.pointFilePath, "a", encoding="utf-8")
        f.write(data)
        f.flush()
        f.close()
        del f

    # 记录断点，传入一个集合
    @classmethod
    def savePointFromSet(cls,setData):
        data=""
        for id in setData:
            data += id + ","
        Point.savePoint(data)



    # 完成爬取
    @classmethod
    def complete(cls):
        overFile = open(cls.overFilePath, "w", encoding="utf-8")
        overFile.write("")
        overFile.flush()
        overFile.close()
        del overFile



ciYunSpider=CiYunSpider()
ciYunSpider.start()