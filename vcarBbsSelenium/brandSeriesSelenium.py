import time,json,re,random,datetime
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy import Selector

# 品牌车系自动化爬取，注意区别与scrapy爬取路径的区别，scrapy从car.autohome.com.cn入口，而此爬虫从www.autohome.com.cn/car入口
# 前者入口只查询出有车型的车系，后者入口包含所有即没有具体车型的也包括进来了

class BrandSeriesSelenium(object):

    # 爬虫入口链接
    url="https://www.autohome.com.cn/car"

    # 插入到数据库的品牌集合
    insertBrandList=list()

    # 插入到数据的车系集合
    insertChexiList=list()

    # 更新车系论坛ID，价格区间
    updateChexiList=list()

    # 插入品牌计数器
    insertBrandCount=0
    # 插入车系计数器
    insertChexiCount=0
    #更新车系计数器
    updateChexiCount=0



    # 初始化
    def __init__(self):
        # 初始化已经存在的品牌id集合
        brandRes=MySqlUtils.query(MySqlUtils.sql_query_brand)
        self.existBrandIdSet=MySqlUtils.parseToSet(brandRes,0)
        # 初始化已经存在的车系集合
        chexiRes=MySqlUtils.query(MySqlUtils.sql_query_chexi)
        self.existChexiIdSet=MySqlUtils.parseToSet(chexiRes,0)

        # 初始化selenium
        self.browser=webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)



    # 爬虫入口
    def start_request(self):
        # 发起请求
        self.requestLink(self.url)
        tab=self.browser.find_element(By.ID,"tab-content")
        letterElementList=tab.find_elements(By.CSS_SELECTOR,".find-letter-list a")
        print("length:%s" % len(letterElementList))
        for i,letterElement in enumerate(letterElementList):
            letter=letterElement.text.strip()
            if i == 0 or letter == None or letter == "热门" or letter == "" :
                continue
            # self.browser.execute_script("arguments[0].scrollIntoView(true);", letterElement)  # 加上这一句即可
            print("i:%s,letter:%s" % (i, letter))
            self.browser.execute_script("arguments[0].click();", letterElement);
            time.sleep(1)

            # 取出page_source
            page_source = self.browser.page_source
            # 转selector取值
            response = Selector(text=page_source)
            # 解析
            self.parse(response,letter)

        # 爬取结束，关闭浏览器
        self.browser.close()





    # 请求
    def requestLink(self,url):
        success = True
        wait = None
        try:
            self.browser.get(url)
            wait = WebDriverWait(self.browser, 10)
            wait.until(EC.presence_of_element_located((By.ID, 'tab-content')))
            time.sleep(0.1)  # 若不加一个会发生页面没有完全渲染
        except Exception as e:
            print(e)
            success = False
        return success


    # 解析
    def parse(self,response,letter):
        # 取出每个每个字母区间的div
        div_id="box%s" % letter
        box=response.css("#%s" % div_id)
        # 一个box下存在多个品牌
        dlList=box.css("#html%s dl" % letter)

        for dl in dlList:
            # 取出品牌id
            brandId=dl.css("::attr(id)").extract_first().strip()
            # 取出品牌图标
            img=dl.css("img ::attr(src)").extract_first().strip()
            img="https:%s" % img
            # 取出品牌名称
            brandName=dl.css("dt div a ::text").extract_first().strip()
            # 取出品牌链接
            brandUrl=dl.css("dt div a ::attr(href)").extract_first()
            brandUrl=brandUrl[:brandUrl.rfind("#")]
            brandUrl="https:%s" % brandUrl
            print()
            print()
            print("===============>品牌:%s,品牌id:%s,img:%s,url:%s" % (brandName,brandId,img,brandUrl))

            # 如果数据库不存在才做保存
            if brandId not in self.existBrandIdSet:
                insertBrandParams=(brandId,letter,brandName,img,brandUrl)
                self.insertBrandList.append(insertBrandParams)
                self.saveBrand()

            # 取出车系类型集
            titList=dl.css(".h3-tit")
            # 取出车系类型下的车系集
            rankList=dl.css(".rank-list-ul")
            for i,tit in enumerate(titList):
                # 取出车系类型
                chexiType=tit.css("a ::text").extract_first()
                # 取出车系信息集
                liList=rankList[i].css("li[id]")
                print("------------>chexiType:%s" % chexiType)

                for li in liList:
                    # 取出车系id
                    chexiId=li.css("::attr(id)").extract_first()
                    chexiId=re.search(r'\d+',str(chexiId)).group()
                    # 取出车系名称
                    chexiName=li.css("h4 a ::text").extract_first()
                    # 取出车系主页链接
                    chexiUrl=li.css("h4 a ::attr(href)").extract_first()
                    chexiUrl=chexiUrl[:chexiUrl.rfind("#")-1]
                    # 是否存在指导价
                    maxPrice=None
                    minPrice=None
                    price=li.css(".red ::text").extract_first()
                    if price:
                        price=li.css("div a ::text").extract_first().strip()
                        maxPrice=price[:price.rfind("-")]
                        minPrice=price[price.rfind("-")+1:price.rfind("万")]
                    # 取出论坛id
                    bbsId=None
                    linkList=li.css("a")
                    for link in linkList:
                        # 取出带论坛的链接
                        linkText=link.css("::text").extract_first()
                        if linkText == "论坛":
                            bbsLink=link.css("::attr(href)").extract_first()
                            bbsId=re.search(r'\d+',bbsLink).group()
                            bbsId="forum-c-%s-1" % bbsId


                    print("chexiName:%s,chexiId:%s,chexiUrl:%s,maxPrice:%s,minPrice:%s" % (chexiName,chexiId,chexiUrl,maxPrice,minPrice))

                    # 如果不存在车系表中，则保存
                    if chexiId not in self.existChexiIdSet:
                        insertChexiParams=(chexiId,brandId,chexiType,chexiName,chexiUrl,maxPrice,minPrice,'2') # 2 表示是否在售状态为未知
                        self.insertChexiList.append(insertChexiParams)
                    else:
                        updateChexiParams=(bbsId,maxPrice,minPrice,chexiId)
                        self.updateChexiList.append(updateChexiParams)



            # 保存车系
            self.saveChexi()











        pass

    # 保存品牌
    def saveBrand(self):
        if len(self.insertBrandList) > 0:
            self.insertBrandCount += len(self.insertBrandList)
            MySqlUtils.updateList(MySqlUtils.sql_insert_brand,self.insertBrandList)
            self.insertBrandList.clear()

        print("saveBrandCount:%s" % self.insertBrandCount)



    # 保存车系
    def saveChexi(self):
        if len(self.insertChexiList) > 0:
            self.insertChexiCount += len(self.insertChexiList)
            MySqlUtils.updateList(MySqlUtils.sql_insert_chexi,self.insertChexiList)
            self.insertChexiList.clear()

        if len(self.updateChexiList) > 0:
            self.updateChexiCount += len(self.updateChexiList)
            MySqlUtils.updateList(MySqlUtils.sql_update_chexi,self.updateChexiList)
            self.updateChexiList.clear()

        print("saveChexiCount:%s,updateChexiCount:%s" % (self.insertChexiCount,self.updateChexiCount))









import pymysql
class MySqlUtils(object):
    #获取数据库链接
    vcar_host="10.1.11.129"


    # 查询品牌表
    sql_query_brand="""
                        SELECT 
                            pinpaiID
                        FROM
                            vcar_vcyber_com.vcar_pinpai;
    """

    # 插入品牌表
    sql_insert_brand="""
                        INSERT INTO `vcar_vcyber_com`.`vcar_pinpai`
                    (`pinpaiID`,
                    `szm`,
                    `name`,
                    `imgUrl`,
                    `url`)
                    VALUES
                    (%s,
                    %s,
                    %s,
                    %s,
                    %s);
    """

    # 查询车系表
    sql_query_chexi="""
                        SELECT 
                            chexiID
                        FROM
                            vcar_vcyber_com.vcar_chexi;
    """
    # 插入车系表
    sql_insert_chexi="""
                        INSERT INTO `vcar_vcyber_com`.`vcar_chexi`
                    (`chexiID`,
                    `pinpaiID`,
                    `chexiType`,
                    `name`,
                    `url`,
                    `maxMoney`,
                    `minMoney`,
                    `onSale`)
                    VALUES
                    (%s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s);
    """

    # 更新论坛id
    sql_update_chexi="""
                        UPDATE vcar_chexi 
                    SET 
                        bbsId = %s,
                        maxMoney=%s,
                        minMoney=%s
                    WHERE
                        chexiId = %s
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


crawler = BrandSeriesSelenium()
crawler.start_request()
