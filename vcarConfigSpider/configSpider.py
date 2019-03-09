#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, re,timeit,random,traceback
from scrapy import Selector




class ConfigSpider(object):
    # 请求计数器
    requestCount=0
    # 保存计数器
    saveCount=0
    # 保存车型数量
    specCount=0
    # 错误计数
    errorCount=0
    # 错误信息格式
    errorModel="{count:%s,class:%s,method:%s,errorInfo:%s}"
    # 当前请求发生错误的链接
    curentLink=""
    # 插入行统计
    rowCount = 0
    # 统计车型数
    totalSpecCount=0

    https = "https:%s"
    host = "https://car.autohome.com.cn%s"
    configLinkModel = "https://car.autohome.com.cn/config/spec/%s.html"

    # 属性分类dict
    shuxingTypeDic = dict()  #
    # 某属性分类下面所有的属性dict集合 {shuxingType:{shuxingName:shuxingValue,,,},,,}
    typeShuxingDic=dict()
    # 车型id的set集合记录已经保存到数据中的车型id，用于判重，若该集合中已存在车型id则证明已经保存过了，无需再请求保存
    specIdSet=set()
    # 车型属性表中已经存在的车型ID，该集合代表已经爬取过的车型
    existChexingIdSet=set()
    # 车型表中所有的id集合,该集合代表所有的车型id
    chexingIdSet=set()

    shuxingDic = dict()  # {"name":"id"}

    browser = webdriver.Chrome()

    def process(self):
        try:
            # 运行开始计时
            startTime=timeit.default_timer()
            # 初始化shuxingTypeDic shuxingDic
            self.shuxingTypeDic = MySqlUtils.queryShuxingType()
            self.typeShuxingDic = MySqlUtils.queryTypeShuxingDic()
            self.shuxingDic = MySqlUtils.queryShuxing()

            # 查询所有的车型id集合
            specLinks=MySqlUtils.querySpecLink()
            self.chexingIdSet=MySqlUtils.parseChexingIdTupeListToSet(specLinks)

            # 查询车型属性表中已存在的车型id集合，即为已爬取过的
            ids=MySqlUtils.queryExistChexingIds()
            self.existChexingIdSet=MySqlUtils.parseChexingIdTupeListToSet(ids)

            # 用所有的车型id集合减去车型属性表中已经存在的车型ID集合，即得出未爬取的车型id集合
            crawlIdSet=self.chexingIdSet - self.existChexingIdSet
            print("chexingIdSet:%s" % len(self.chexingIdSet))
            print(("existChexingIdSet:%s" % len(self.existChexingIdSet)))
            print("------------------------>本次需爬取车型数量为：%s" % len(crawlIdSet))

            for item in specLinks:
                # 如果不存在于待爬id集合中，则证明已经爬取过 不用再爬
                if item[0] not in crawlIdSet:
                    continue

                # 检测该车型ID在车型属性数据中是否存在，若已存在则证明已经爬过不用再重复爬取
                # isInsert=MySqlUtils.queryChexingShuxingById((item[0])) # todo 优化地方：当车型属性表数据量达到百万级后查询时会有损效率，可以考虑将爬过的车型id保存到redis中，或者mysql临时表中，或者使用set集合
                exist = item[0] in self.specIdSet
                if exist :
                    continue

                circleStartTime = timeit.default_timer()

                # 2、摸拟浏览器请求获取页面
                configUrl = self.configLinkModel % item[0]

                step1Time=timeit.default_timer()
                if not self.requestConfigLink(configUrl):
                    #请求超时，证明没有数据，返回请求下一个
                    print("请求超时")
                    self.specIdSet.add(item[0])
                    continue

                # 解析出页面所有的span
                classNameSet=self.parseSpanClassName()

                # 将伪元素翻译成页面上的显式值
                step2Time=timeit.default_timer()
                self.translatePage(classNameSet)

                # 取出最新的page_source
                page_source=self.browser.page_source

                # 将page_source装入到Selector中
                page=Selector(text=page_source)

                # 解析导航栏中车型id
                chexingIdList=self.parseChexingIdList(page)

                # 定位数据table所在的div
                dataDiv=page.css("#config_data")

                # 定位table
                tableList=dataDiv.xpath("table[@id]")

                # 提取值并保存到数据库
                step3Time=timeit.default_timer()
                self.parseTable(chexingIdList,tableList)

                # 统计一次完整请求解析入库的时间
                circleEndTime=timeit.default_timer()
                print("onecircleCastTime--> %s  requestCastTime-->%s  translateCastTime-->%s  parseTableAndSaveCastTime-->%s" % (str(circleEndTime-circleStartTime),str(step2Time-step1Time),str(step3Time-step2Time),str(circleEndTime-step3Time)))
            endTime = timeit.default_timer()
            print(round(endTime-startTime))
        except Exception as e:
            print(traceback.print_exc())
            self.errorCount += 1
            error = self.errorModel % (self.errorCount, "configSpider", "process", str(e))
            self.writeError(error)



    # 请求车型配置页面
    def requestConfigLink(self, configUrl):
        try:
            #configUrl="https://car.autohome.com.cn/config/spec/20211.html" #该请求没有配置数据
            self.requestCount+=1
            self.browser.get(configUrl)
            wait = WebDriverWait(self.browser, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tbcs')))
            time.sleep(0.1)  # 若不加一个会发生页面没有完全渲染
            self.curentLink=configUrl
            return True
        except Exception as e:
            return False

    # 解析导航栏中各车型id
    def parseChexingIdList(self,page):
        # 获取导航栏中车型id
        chexingIdList=list()
        try:
            tableNavTdList=page.css(".tbset").xpath(".//tr").xpath(".//td")
            for td in tableNavTdList:
                href=td.xpath("div/div/a/@href").extract_first()
                #print(href)
                if href:
                    id=href[href.find("spec/") + 5:href.find("/#")]
                    chexingIdList.append(id)
                    #向已爬取车型集合中添加车型id，用于判重
                    self.specIdSet.add(id)
            # print(chexingIdList)
            self.specCount+=len(chexingIdList)
        except Exception as e:
            self.errorCount += 1
            error = self.errorModel % (self.errorCount, "configSpider", "parseChexingIdList", str(e))
            self.writeError(error)
        return chexingIdList




    # 解析伪元素class，获取className不重复的集合
    def parseSpanClassName(self):
        # 定义存放className的set集合
        classNameSet=set()
        try:
            # 取出page_source
            page_source=self.browser.page_source
            # 转selector取值
            page=Selector(text=page_source)
            # 定位table所在的div
            dataDiv=page.css("#config_data")
            # 定位div中所有的span
            spanList=dataDiv.xpath(".//span[@class]")
            for span in spanList:
                #print(span.xpath("@class").extract_first())
                className=span.xpath("@class").extract_first()
                if className and re.match(r'^\w*_\w*_\w*$',className):
                    classNameSet.add(className)
        except Exception as e:
            self.errorCount += 1
            error = self.errorModel % (self.errorCount, "configSpider", "parseSpanClassName", str(e))
            self.writeError(error)
        return classNameSet



    # 翻译整个页面伪元素
    def translatePage(self,classNameSet):
        classNameRecorde = ""
        try:
            # 执行js，根据className取值，再显式赋值
            preGetImplicitContentJs="return window.getComputedStyle(document.getElementsByClassName('%s')[0], 'before').getPropertyValue('content')"
            preSetViewableContenJs = """
                              var arr = document.getElementsByClassName('%s');
                              if (arr != undefined && arr.length > 0){
                                  for(i=0;i<arr.length;i++){
                                       arr[i].innerHTML=%s;
                                  }
                               }
                            """
            for className in classNameSet:

                classNameRecorde=className
                getImplicitContentJs=preGetImplicitContentJs % className
                content=self.browser.execute_script(getImplicitContentJs)
                #print(content)
                # 再次执行js，反向回显内容
                setViewableContenJs=preSetViewableContenJs % (className,content)
                self.browser.execute_script(setViewableContenJs)
            # 页面翻译完成
        except Exception as e:
            self.errorCount += 1
            error = self.errorModel % (self.errorCount, "configSpider", "translatePage", "url->"+self.curentLink+",spanClassName->"+classNameRecorde+","+str(e))
            self.writeError(error)

    def parseTable(self,chexingIdList,tableList):
        shuxingCount=0
        try:
            paramsList = list()
            for table in tableList:
                #print(table.xpath("@id").extract_first()+"-->"+table.xpath("tbody/tr[1]/th/h3/span/text()").extract_first())
                # 取出tr/html/body/div[3]/div[3]/table[3]/tbody/tr[1]/th/h3
                trList=table.xpath(".//tr")
                shuxingTypeName = ""
                shuxingTypeId = ""
                # 定义车型属性集合，作为插入数据库中的参数
                shuxingDic = dict()
                for index,tr in enumerate(trList):
                    shuxingName = ""
                    shuxingId = ""
                    # 第一个是属性类别
                    if index == 0:
                        shuxingTypeName=tr.xpath("string(.)").extract_first()
                        shuxingTypeId=self.shuxingTypeDic.get(shuxingTypeName)
                        # 根据属性类别名既可以取出该类别下所有的属性
                        shuxingDic=self.typeShuxingDic.get(shuxingTypeName)
                        # 如果属性字典为None则需要完善属性类和属性
                        if not shuxingDic:
                            filename = "/Users/guohan/DeskTop/shuxingError.txt"
                            error = "{url:%s,shuxingTypeName:%s}" % (chexingIdList[0],shuxingTypeName)
                            with open(filename, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                                f.write(error)
                                f.flush()
                                f.close()
                        continue

                    # 解析属性名和属性值
                    tdList=tr.xpath("*")
                    for i,td in enumerate(tdList):
                        # 第一个td就是属性名，后面的都是属性值
                        if i == 0 :
                            shuxingCount+=1
                            shuxingName=td.xpath("string(.)").extract_first()
                            # 根据属性名获取属性id
                            if shuxingDic:
                                shuxingId = shuxingDic.get(shuxingName)
                            # 若发现属性表中未定义该属性字段，则自动插入一条属性
                            if (shuxingId == None or shuxingId == "") and shuxingName != '外观颜色' and shuxingName != '内饰颜色' and shuxingTypeName != "选装包":
                                shuxingId=shuxingTypeId+"_"+ str(round(time.time() * 1000000))
                                insertParams=(shuxingId,shuxingTypeId,shuxingName)
                                MySqlUtils.insertOneShuxing(insertParams)
                                shuxingDic.setdefault(shuxingName,shuxingId)
                            #print(shuxingName,shuxingId)
                            continue

                        # 解析属性值
                        if i-1 < len(chexingIdList):
                            # 如果是外观或内饰颜色，则单独取值
                            if shuxingName == '外观颜色' or shuxingName == '内饰颜色':
                                shuxingId = self.typeShuxingDic.get('车身/内饰颜色').get(shuxingName)
                                shuxingTypeId=self.shuxingTypeDic.get('车身/内饰颜色')
                                # 每种颜色用中文名和颜色值表示，用冒号分隔，一组颜色用分号分隔，不同组之间用逗号分隔，示例： 颜色中文名:颜色rgb值,颜色rgb值;颜色中文名:颜色rgb值
                                colors=""
                                liList=td.xpath(".//li")
                                for li in liList:
                                    colorName=None
                                    if li.xpath("a/@title").extract_first():
                                        colorName=li.xpath("a/@title").extract_first()
                                    elif li.xpath("span/@title").extract_first():
                                        colorName=li.xpath("span/@title").extract_first()
                                    colorGroup=colorName+":"
                                    emList=li.xpath("span/em[@style]")

                                    for em in emList:
                                        style=em.xpath("@style").extract_first()
                                        colorGroup+=style[style.find(":")+1:style.find(";")]+","
                                    colorGroup=colorGroup.rstrip(",")
                                    colors+=colorGroup+";"

                                shuxingValue=colors.rstrip(";")
                                # print("---------------------%s-----------------" % colors)
                            elif not shuxingTypeId:
                                continue
                            else:
                                shuxingValue = td.xpath("string(.)").extract_first()

                            # 检测\ax0
                            shuxingValue="".join(shuxingValue.split())

                            # print("lllllllllllllllll:"+str(len(chexingIdList))+"   iiiiiiiiiiiiii:"+str(i-1))
                            #print("values-->:",chexingIdList[i-1],shuxingTypeId,shuxingId)
                            chexingShuxingId=chexingIdList[i-1]+"_"+ shuxingTypeId+"_"+shuxingId+"_"+str(random.randint(0,10000))
                            valueTupe=(chexingShuxingId,chexingIdList[i-1],shuxingId,shuxingName,shuxingValue) #(车型属性表ID，车型id，属性id，属性名，属性值)
                            paramsList.append(valueTupe)
                            self.rowCount += 1
                            #print(valueTupe)

                    #print("shuxingName:%s,shuxingId:%s,self.rowCount:%s" % (shuxingName,shuxingId,self.rowCount))

                # 保存到数据库
                self.saveCount += 1
                # print("saveCount--------------------------> %s" % self.saveCount)
            MySqlUtils.insertChexingShuxing(paramsList)
            print("saveCount:%s ,saveSpecCount: %s  ,shuxingCount: %s ,rowCount: %s" % (self.saveCount,self.specCount,shuxingCount,self.rowCount))
        except Exception as e:
            print(traceback.print_exc())
            self.errorCount+=1
            error=self.errorModel % (self.errorCount,"configSpider","parseTable",str(e))
            self.writeError(error)



    def writeError(self,error):
        filename="/Users/guohan/DeskTop/error.txt"
        with open(filename, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
            f.write(error)
            f.flush()
            f.close()


import pymysql, timeit


class MySqlUtils(object):
    errorModel = "{count:%s,class:%s,method:%s,errorInfo:%s}"
    errorCount = 0
    vcar_host = "10.1.11.129"
    var_password = '12345'

    # 获取数据库链接
    @classmethod
    def getConnection(cls):
        conn = pymysql.connect(host='localhost', user='root', passwd='root', db='vcar_vcyber_com', port=3306,
                               charset='utf8')
        return conn

    @classmethod
    def queryBrandId(cls):
        # self.log("start query --------------------------------")
        queryList = list()
        try:
            conn = cls.getConnection()
            cur = conn.cursor()
            sql = """
            SELECT  `vcar_pinpai`.`pinpaiID`
            FROM `vcar_vcyber_com`.`vcar_pinpai`;
            """
            cur.execute(sql)
            res = cur.fetchall()
            # for item in res:
            # print(item)
            # self.log(item)
            # 返回的是列表，列表元素类型是元组[(),(),,]
            return res

        except Exception as e:
            pass
            # print(e)
            # self.log(e)
            # self.log("查询失败")
        finally:
            cur.close()
            conn.close()
        # self.log("end query ----------------------------------")

    # 查询车系信息，返回元组(brandId,seriesId,seriesLink)
    @classmethod
    def querySeriesLink(cls):
        sql = """
                SELECT 
                    `vcar_chexi`.`pinpaiID`,
                    `vcar_chexi`.`chexiID`,
                    `vcar_chexi`.`url`
                FROM `vcar_vcyber_com`.`vcar_chexi`;
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行查询
            cursor.execute(sql)
            # 获取结果
            res = cursor.fetchall()
            # for item in res:
            #    print(item)
            return res
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    # 查询车型链接信息
    @classmethod
    def querySpecLink(self):
        sql = """
                SELECT `vcar_chexing`.`chexingID`,
                        `vcar_chexing`.`pinpaiID`,
                        `vcar_chexing`.`chexiID`,
                        `vcar_chexing`.`name`,
                        `vcar_chexing`.`url`
                FROM `vcar_vcyber_com`.`vcar_chexing`;
        """
        try:
            conn = self.getConnection()
            cursor = conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            # for item in res:
            #     print(item)
            return res
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    # 返回一个以属性id为key，属性名为value的字典
    @classmethod
    def queryShuxing(cls):
        sql = """
                SELECT `vcar_shuxing`.`shuxingID`,
                       `vcar_shuxing`.`name`
                FROM `vcar_vcyber_com`.`vcar_shuxing`;
            """
        try:
            if id:
                conn = cls.getConnection()
                cursor = conn.cursor()
                cursor.execute(sql)
                res = cursor.fetchall()
                # 转为Dic数据类型
                shuxingDic = dict()
                for item in res:
                    shuxingDic.setdefault(item[1], item[0])
                return shuxingDic
            else:
                return None
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    # 查询属性类型表返回以属性名作为key，属性id为value的字典
    @classmethod
    def queryShuxingType(cls):
        sql = """
                SELECT 
                    `vcar_shuxingtype`.`name`,
                    `vcar_shuxingtype`.`shuxingTypeID`
                  FROM `vcar_vcyber_com`.`vcar_shuxingtype`;
        """
        try:
            conn = cls.getConnection()
            cursor = conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            # 转Dict数据类型
            typeDict = dict()
            for item in res:
                typeDict.setdefault(item[0], item[1])
            return typeDict
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    # 查询属性type下的属性集合{shuxingType:{shuxingName:shuxingValue,,,},,,}
    @classmethod
    def queryTypeShuxingDic(cls):
        typeDic = cls.queryShuxingType()
        sql = """
                 SELECT `vcar_shuxing`.`shuxingID`,
                       `vcar_shuxing`.`name`
                 FROM `vcar_vcyber_com`.`vcar_shuxing` 
                 where shuxingTypeID=%s       
        """
        typeShuxingDic = dict()
        try:
            conn = cls.getConnection()
            cursor = conn.cursor()
            for key in typeDic.keys():
                typeId = typeDic.get(key)
                cursor.execute(sql, typeId)
                res = cursor.fetchall()
                shuxingDic = dict()
                for item in res:
                    shuxingDic.setdefault(item[1], item[0])
                typeShuxingDic.setdefault(key, shuxingDic)
            return typeShuxingDic
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    # 插入到属性表
    @classmethod
    def insertIntoShuxing(cls, params):
        sql = """
                INSERT INTO `vcar_vcyber_com`.`vcar_shuxing`
                    (`shuxingID`,
                    `shuxingTypeID`,
                    `name`)
                    VALUES
                    (%s,
                    %s,
                    %s);
        """
        try:
            conn = cls.getConnection()
            cursor = conn.cursor()
            res = cursor.executemany(sql, params)
            conn.commit()
            return res
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    @classmethod
    def queryChexingShuxingById(cls, id):
        startTime = timeit.default_timer()
        sql = """
                SELECT 
            `vcar_chexingshuxing`.`chexingID`
        FROM `vcar_vcyber_com`.`vcar_chexingshuxing`
        where chexingID=%s;
        """
        try:
            conn = cls.getConnection()
            cursor = conn.cursor()
            cursor.execute(sql, id)
            res = cursor.fetchone()
            endTime = timeit.default_timer()
            print("queryIsInsertCastTime------------------->: %s" % str(endTime - startTime))
            if res:
                return True
            else:
                return False
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    @classmethod
    def insertOneShuxing(cls, params):
        sql = """
            INSERT INTO `vcar_vcyber_com`.`vcar_shuxing`
                (`shuxingID`,
                `shuxingTypeID`,
                `name`)
                VALUES
                (%s,
                 %s,
                 %s);
        """
        try:
            conn = cls.getConnection()
            cursor = conn.cursor()
            i = cursor.execute(sql, params)
            conn.commit()
            return i
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    # 向车型属性表中插入数据
    @classmethod
    def insertChexingShuxing(cls, paramsList):
        startTime = timeit.default_timer()
        sql = """
                INSERT INTO 
                    `vcar_vcyber_com`.`vcar_chexingshuxing`
                    (`chexingshuxingID`,
                    `chexingID`,
                    `shuxingID`,
                    `shuxingName`,
                    `shuxingValue`)
                    VALUES
                    (%s,
                    %s,
                    %s,
                    %s,
                    %s);
        """
        try:
            conn = cls.getConnection()
            cursor = conn.cursor()
            # print(paramsList)
            res = cursor.executemany(sql, paramsList)
            conn.commit()
            endTime = timeit.default_timer()
            print("insertChexingShuxingCastTime------------------------>:%s" % str(endTime - startTime))
        except Exception as e:
            print(e)
            cls.errorCount += 1
            filename = "/Users/guohan/DeskTop/mySqlError.txt"
            error = cls.errorModel % (cls.errorCount, "MySqlUtils", "insertChexingShuxing", str(e))
            with open(filename, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(error)
                f.flush()
                f.close()
        finally:
            conn.close()
            cursor.close()

    # 查询已爬取过配置的车型id
    @classmethod
    def queryExistChexingIds(cls):
        sql = """     
            SELECT distinct(t.chexingID) 
            FROM vcar_vcyber_com.vcar_chexingshuxing t 
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql)
            # 提交
            conn.commit()
            res = cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    # 将上一个查询车型id方法返回值转换为list
    @classmethod
    def parseChexingIdTupeListToSet(cls, res):
        chexingIdSet = set()
        for item in res:
            chexingIdSet.add(item[0])
        print(chexingIdSet)
        return chexingIdSet


#
# my = MySqlUtils()
# res=my.queryExistChexingId()
# my.parseChexingIdTupeListToSet(res)
# name="基本参数"
# typeDict=my.queryShuxingType()
# keys=typeDict.keys()
# # for key in keys:
# #     print(key,typeDict[key])
# shuxingDict=my.queryShuxing()
# shuxingKeys=shuxingDict.keys()
# for key in shuxingKeys:
#     print(key,shuxingDict[key])
# typeDic=MySqlUtils.queryShuxingType()
# print(typeDic)
# print(MySqlUtils.queryTypeShuxingDic())


print('<-------------------start----------------->')
sc = ConfigSpider()
sc.process()
