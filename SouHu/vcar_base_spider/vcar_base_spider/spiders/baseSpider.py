
import scrapy,pymysql,re,time,requests,datetime,random
from ..mySqlUtils import MySqlUtils
class BaseSpider(scrapy.Spider):

    name = "baseSpider"
    # 插入品牌表集合
    insertBrandList=list()
    # 更新品牌表集合
    updateBrandList=list()

    # 插入车系类别表集合
    insertChexiTypeList=list()
    # 更新车系类别表集合
    updateChexiTypeList=list()

    # 插入车系表集合
    insertChexiList=list()
    # 更新车系集合
    updateChexiList=list()

    # 统计插入品牌数量
    insertBrandCount=0
    # 统计插入车系类别数量
    insertChexiTypeCount=0
    # 统计插入车系数量
    insertChexiCount=0

    # 统计保存车系销量数据
    insertChexiSalesCount=0



    def __init__(self):
        # 查询已经存在的品牌车系类别及车系
        brandRes = MySqlUtils.query(MySqlUtils.sql_query_brand)
        self.existBrandIdSet = MySqlUtils.parseToSet(brandRes, 0)
        # 查询已经存在的车系类别
        chexiTypeRes = MySqlUtils.query(MySqlUtils.sql_query_chexi_type)
        self.existChexiTypeIdSet = MySqlUtils.parseToSet(chexiTypeRes, 0)
        # 查询已经存在的车系
        chexiRes = MySqlUtils.query(MySqlUtils.sql_query_chexi)
        self.existChexiIdSet = MySqlUtils.parseToSet(chexiRes, 0)
        # 查询已存在的车系销量字典，由于数据量比较大，因此采用车系id作为key，日期集合为value的字典
        self.chexiSalesDict=self.initChexiSales()
        # print(self.chexiSalesDict)



    # 初始化销量字典，用于判重
    def initChexiSales(self):
        chexiSalesRes = MySqlUtils.query(MySqlUtils.sql_query_chexi_sales)
        chexiSalesDict=dict()
        for chexiSales in chexiSalesRes:
            chexiId=chexiSales[0]
            countDate=chexiSales[1].strftime('%Y-%m-%d')
            # print(countDate)
            salesNum=chexiSalesRes[2]
            if chexiSalesDict.get(chexiId):
                monthList=chexiSalesDict.get(chexiId)
                monthList.append(countDate)
            else:
                monthList=list()
                monthList.append(countDate)
                chexiSalesDict.__setitem__(chexiId,monthList)
        return chexiSalesDict


    # 请求入口
    def start_requests(self):
        url="http://db.auto.sohu.com/home/"
        request=scrapy.Request(url=url,callback=self.parse)
        yield request



    # 解析品牌车系树
    def parse(self, response):
        liList=response.css(".tree li")
        letter=None
        # 插入品牌集合
        insertPinPaiList=list()
        # 插入车系类别集合
        insertChexiTypeList=list()
        # 插入车系集合
        insertChexiList=list()
        # 车系ID集合，用于请求销量
        chexiIdSet=set()
        # 品牌集合，用于按品牌请求保存该品牌下的车系代表图片
        brandIdSet=set()
        for li in liList:
            liClassName=li.css("::attr(class)").extract_first()
            if liClassName == "tree_tit":
                # 取出首字母
                letter=li.css("::text").extract_first()
            else:
                # 取出品牌名称
                brandName=li.xpath("h4/a").xpath("string(.)").extract_first()
                if brandName:
                    brandName=brandName.strip()
                # 取出品牌链接
                brandLink=li.css("a ::attr(href)").extract_first()
                # 取出品牌id
                brandId=re.search(r'\d+',brandLink).group()
                # 添加到品牌集合中
                brandIdSet.add(brandId)
                # 封装插入品牌表参数
                insertPinPaiParams=(brandId,letter,brandName,brandLink)
                if brandName and  brandId not in self.existBrandIdSet and insertPinPaiParams not in insertPinPaiList:
                    print(insertPinPaiParams)
                    insertPinPaiList.append(insertPinPaiParams)

                # 取出车系列表
                chexiLiList=li.css(".tree_con li")
                chexiType=None
                chexiTypeId=None

                for chexiLi in chexiLiList:
                    #取出车系类别及其id
                    if chexiLi.css("::attr(class)").extract_first().strip() == "con_tit":
                        chexiType=chexiLi.xpath("a").xpath("string(.)").extract_first().strip()
                        chexiTypeLink=chexiLi.css("a ::attr(href)").extract_first()
                        chexiTypeId=re.search(r'\d+',chexiTypeLink).group()
                        continue
                    # 取出车系链接
                    chexiLink=chexiLi.css("a ::attr(href)").extract_first().strip()
                    # 取出车系id
                    numArr=re.findall(r'\d+',chexiLink)
                    chexiId=None
                    if len(numArr) == 1:
                        chexiId=numArr[0]
                    else:
                        chexiId=numArr[1]
                    # 添加到车系id集合中
                    chexiIdSet.add(chexiId)
                    # 取出车系名称
                    chexiName=chexiLi.xpath("a").xpath("string(.)").extract_first().strip()
                    # print("letter:%s,brandName:%s,brandId:%s,brandLink:%s,typeName:%s,typeId:%s,chexiName:%s,chexiId:%s,chexiLink:%s" % (letter,brandName,brandId,brandLink,chexiType,chexiTypeId,chexiName,chexiId,chexiLink))
                    # 封装车系参数
                    if chexiId not in self.existChexiIdSet:
                        insertChexiParams=(chexiId,brandId,chexiType,chexiTypeId,chexiName,chexiLink)
                        insertChexiList.append(insertChexiParams)
                    # 封装车系类别参数
                    insertChexiTypeParams = (chexiTypeId, chexiType, brandId)
                    if chexiTypeId not in self.existChexiTypeIdSet and insertChexiTypeParams not in insertChexiTypeList :
                        # print(insertChexiTypeParams)
                        insertChexiTypeList.append(insertChexiTypeParams)
                        flag=False
        # 保存入库
        self.saveBrandAndChexi(insertPinPaiList,insertChexiTypeList,insertChexiList)

        # 请求品牌，解析该品牌下车系代表图片小图
        for brandId in brandIdSet:
            url="http://db.auto.sohu.com/brand_%s/home/iframe.html" % brandId
            request=scrapy.Request(url=url,callback=self.parseChexiPriceAndImg)
            yield request

        # 请求销量
        for chexiId in chexiIdSet:
            url="http://db.auto.sohu.com/cxdata/xml/sales/model/model%ssales.xml" % chexiId
            request=scrapy.Request(url=url,callback=self.parseSales)
            request.meta['chexiId']=chexiId
            yield request


    # 解析该品牌下的车系价格区间，在售停售状态，代表图片
    def parseChexiPriceAndImg(self,response):
        tabDiv=response.css(".tabcon.cur")
        chexiLiList=tabDiv.css(".ptlist li")
        for chexiLi in chexiLiList:
            # 解析车系id
            chexiLink=chexiLi.css("a ::attr(href)").extract_first()
            chexiId=re.search(r'\d+',chexiLink).group()
            # 解析车系图片
            imgUrl=chexiLi.css("img ::attr(src)").extract_first()
            # 解析价格区间
            priceStr=chexiLi.css(".red a ::text").extract_first()
            priceSection=re.findall("(\d+\.\d+)+", priceStr)
            minPrice=None
            maxPrice=None
            if priceSection:
                minPrice=priceSection[0]
                maxPrice=priceSection[1]
            # 解析在售停售状态
            onSale="1"
            stop=chexiLi.css(".tip_stop")
            if stop:
                onSale="0"



    # 解析该车系的销量
    def parseSales(self,response):
        chexiId=response.meta['chexiId']
        monthSales=response.css("model sales")
        if monthSales:
            insertChexiSalesList=list()
            for monthSale in monthSales:
                # 取出日期
                monthDate=monthSale.css("::attr(date)").extract_first()
                # 取出销量
                saleNum=monthSale.css("::attr(salesNum)").extract_first()
                # print("chexiId:%s,---------monthDate:%s  ,saleNum:%s" % (chexiId,monthDate,saleNum))
                sid="%s_%s_%s" % (chexiId,monthDate,random.randint(10000,99999))
                insertParams=(sid,chexiId,saleNum,monthDate)
                # 判重
                if not self.chexiSalesDict.get(chexiId):
                    insertChexiSalesList.append(insertParams)
                else:
                    monthList=self.chexiSalesDict.get(chexiId)
                    if monthDate not in monthList:
                        insertChexiSalesList.append(insertParams)

            # 保存到数据库
            self.saveChexiSales(insertChexiSalesList)

    # 保存品牌、车系类别、车系
    def saveBrandAndChexi(self,insertPinPaiList,insertChexiTypeList,insertChexiList):
        if len(insertPinPaiList) > 0:
            MySqlUtils.updateList(MySqlUtils.sql_insert_brand,insertPinPaiList)
            self.insertBrandCount += len(insertPinPaiList)
            insertPinPaiList.clear()

        if len(insertChexiTypeList) > 0:
            MySqlUtils.updateList(MySqlUtils.sql_insert_chexi_type,insertChexiTypeList)
            self.insertChexiTypeCount += len(insertChexiTypeList)
            insertChexiTypeList.clear()

        if len(insertChexiList) > 0:
            MySqlUtils.updateList(MySqlUtils.sql_insert_chexi,insertChexiList)
            self.insertChexiCount += len(insertChexiList)
            insertChexiList.clear()

        print("~~~~~~~~~~~~~~~~insertBrandCount:%s~~~~~~~~~~insertChexiTypeCount:%s~~~~~~~~~~~~~~~~insertChexiCount:%s" % (self.insertBrandCount,self.insertChexiTypeCount,self.insertChexiCount))


    # 保存车系销量到数据库
    def saveChexiSales(self,insertList):
        if len(insertList) > 0:
            MySqlUtils.updateList(MySqlUtils.sql_insert_chexi_sales,insertList)
            self.insertChexiSalesCount += len(insertList)
            insertList.clear()
            print("===================>insertChexiSalesList:%s" % self.insertChexiCount)

