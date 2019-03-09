
import scrapy,pymysql,re
from ..mySqlUtils import MySqlUtils
from ..items import SpecItem,SeriesItem
from ..pipelines import SpecPipeline

#请求车系下的车型列表信息，完善
class specSpider(scrapy.Spider):
    name = "specSpider"
    https="https:%s"
    host="https://car.autohome.com.cn%s"
    count=0
    ruleId=2 # 爬取策略：1为只爬取数据库中不存在的，2是全部更新
    chexingIdSet=None #重数据库查出的已爬取的车型id集合

    # 解析车型列表数据，并保存到数据库
    def parseSpec(self, response):
        # 解析
        seriesParams = response.meta['seriesParams']
        specList=self.extractSpecItem(response)
        # 保存到数据库
        for specItem in specList:
            yield specItem

        #当前页面解析完成后判断是否存在分页，若存在分页则继续请求分页链接，再解析到本方法中
        pageData = response.css(".page")
        if pageData:
            #取出nextPage
            pageList = pageData.xpath("a")
            nextPage=pageList[len(pageList) - 1].xpath("@href").extract_first()
            #若存在有效的下一页链接，则继续请求
            if nextPage.find("java") == -1:
                pageLink = self.host % nextPage
                request = scrapy.Request(url=pageLink, callback=self.parseSpec)
                request.meta['seriesParams'] = seriesParams  # (品牌ID，车系id)
                yield request



    #解析车系车型信息
    def parse(self, response):

        seriesItem=SeriesItem()
        seriesParams=response.meta['seriesParams']

        #解析车系概要信息
        seriesData = response.css(".lever-ul").xpath("*")
        #解析车辆级别
        lever=seriesData[0].xpath("string(.)").extract_first() #'级\xa0\xa0别：中型SUV'
        lever=lever.split("：")[1].strip()
        # 解析指导价
        minPrice = 0
        maxPrice = 0
        seriesDataRight = response.css(".main-lever-right").xpath("*")
        price = seriesDataRight[0].xpath("span/span/text()").extract_first()
        if price.find("-") != -1:
            price = price.rstrip("万")
            price = price.split("-")
            minPrice = price[0]
            maxPrice = price[1]
        # 解析用户评分
        userScore = 0
        userScoreStr = seriesDataRight[1].xpath("string(.)").extract_first()
        if re.search(r'\d+', userScoreStr) != None:
            userScore = userScoreStr.split("：")[1]
        #保存车系概要信息到数据库
        seriesItem['minMoney']=minPrice
        seriesItem['maxMoney']=maxPrice
        seriesItem['score']=userScore
        seriesItem['jibie']=lever
        seriesItem['chexiID']=seriesParams[1]
        # self.log(seriesItem)
        yield seriesItem

        # 解析当前车型页面
        specList = self.extractSpecItem(response)
        # self.log(specList)
        # 保存到数据库
        for specItem in specList:
            yield specItem


        #解析车型概要信息
        #爬取逻辑：
        #   1、获取在售、即将销售、停售三种状态
        #   2、依次判断每个状态是否有值，若有值，则判断当前页面是否为直接进入的
        #   3、解析当前状态数据
        #   4、当存在分页时继续请求

        # 1.1 定义三种链接
        sellingLink='-1'   #在售
        sellWaitLink='-1'  #即将销售
        sellStopLink='-1'  #停售
        # 1.2 取出三种状态
        statusData = response.css(".tab-nav.border-t-no")
        statusList = statusData.xpath("ul/li")
        for statusItem in statusList:
            status = statusItem.xpath("a")
            if status:
                statusDes=status.xpath("text()").extract_first()
                link=status.xpath("@href").extract_first()
                if statusDes == '在售':
                    sellingLink=link
                if statusDes == '即将销售':
                    sellWaitLink=link
                if statusDes == '停售':
                    sellStopLink=link
        # self.log("-------------------------->status")
        statusPrint=(sellingLink,sellWaitLink,sellStopLink)
        # self.log(statusPrint)

        # 2.2 判断即将销售状态
        if sellWaitLink != '-1':
            #若在售有值则证明不是直接请求过来的，则发起请求，否则就是直接请求过来的直接解析
            if sellingLink != '-1':
                #发送请求
                request = scrapy.Request(url=self.host % sellWaitLink, callback=self.parseSpec)
                request.meta['seriesParams'] = seriesParams  # (品牌ID，车系id)
                yield request
        # 2.3 判断停售状态
        if sellStopLink != '-1':
            #判断在售状态或即将销售状态是否有值，若有值则证明不是直接请求过来的需要请求后才能解析，若有没有值则直接请求过来的，直接解析即可，
            if sellingLink != '-1' or sellWaitLink != '-1':
                #请求链接
                request = scrapy.Request(url=self.host % sellStopLink, callback=self.parseSpec)
                request.meta['seriesParams'] = seriesParams  # (品牌ID，车系id)
                yield request
            else:
                # 判断是否存在分页，若存在则继续请求
                pageData = response.css(".page")
                if pageData:
                    # 取出nextPage
                    pageList = pageData.xpath("a")
                    nextPage = pageList[len(pageList) - 1].xpath("@href").extract_first()
                    # 若存在有效的下一页链接，则继续请求
                    if nextPage.find("java") == -1:
                        pageLink = self.host % nextPage
                        request = scrapy.Request(url=pageLink, callback=self.parseSpec)
                        request.meta['seriesParams'] = seriesParams  # (品牌ID，车系id)
                        yield request


    def start_requests(self):
        self.chexingIdSet=MySqlUtils.parseToChexingIdSet(MySqlUtils.querySpec())
        # 读取数据库车系表，获取访问车系车型链接
        seriesItems = MySqlUtils.querySeriesLink()
        # seriesItems=["https://car.autohome.com.cn/price/series-4171.html"] # 测试停售
        # seriesItems=["https://car.autohome.com.cn/price/series-4887.html"] # 测试即将销售 具体车型ID：35775
        # 从断点处开始爬取
        waitingCrawlItems = list()
        for id in SpecPipeline.waitingCrawlSeriesIdSet:
            for item in seriesItems:
                if id == item[1]:
                    waitingCrawlItems.append(item)
                    break
        #waitingCrawItems=MySqlUtils.findChexiInChexiSet(seriesItems,SpecPipeline.waitingCrawlSeriesIdSet)

        for item in waitingCrawlItems:
            # 统计已爬取的车系
            SpecPipeline.crawledSeriesCount += 1
            SpecPipeline.crawledSeriesIdSet.add(item[1])
            url=item[2]
            # url = item
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['seriesParams'] = (item[0], item[1])  # (品牌ID，车系id)
            # request.meta['seriesParams'] = ('122', '4887')  # (品牌ID，车系id)
            yield request







    # 封装取出车型集合
    def extractSpecItem(self,response):
        # 解析
        seriesParams = response.meta['seriesParams']
        specDataGroups = response.css(".interval01-list")
        specList=list()
        for specDataGroup in specDataGroups:
            for specDataItem in specDataGroup.xpath("li"):
                # 车型id
                specId = specDataItem.xpath("@data-value").extract_first()
                specNameData = specDataItem.css("#p" + specId).xpath("a")
                # 车型名称
                specName = specNameData.xpath("text()").extract_first()
                # 车型链接
                specLink = self.https % specNameData.xpath("@href").extract_first()

                specLink=specLink[0:specLink.find("#")-1]
                specItem = SpecItem()
                specItem['pinpaiID'] = seriesParams[0]
                specItem['chexiID'] = seriesParams[1]
                specItem['chexingID'] = specId
                specItem['name'] = specName
                specItem['url'] = specLink
                specItem['sqlType'] = '1'
                # self.log(specItem)
                # 统计新增车型
                if specId not in self.chexingIdSet:
                    SpecPipeline.addSpecCount += 1
                # ruleId等于1时只更新新增的车型，已存在的不会做更新
                if self.ruleId == 1:
                    if specId in self.chexingIdSet:
                        continue

                self.log("yieldCount：%d" % self.count)
                # 保存车型到数据库
                self.count += 1
                specList.append(specItem)

        return specList




    # 批量保存到数据库
    # def parseSellingSpec(self,response):
    #     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>parseSellingSpec")
    #     t=type(response)
    #     self.log(t)
    #     # 解析
    #     seriesParams = response.meta['seriesParams']
    #     specDataGroups = response.css(".interval01-list")
    #     self.log(seriesParams)
    #     self.log(specDataGroups)
    #     specList=list()
    #     for specDataGroup in specDataGroups:
    #         for specDataItem in specDataGroup.xpath("li"):
    #             # 车型id
    #             specId = specDataItem.xpath("@data-value").extract_first()
    #             specNameData = specDataItem.css("#p" + specId).xpath("a")
    #             # 车型名称
    #             specName = specNameData.xpath("text()").extract_first()
    #             # 车型链接
    #             specLink = self.https % specNameData.xpath("@href").extract_first()
    #             pingpaiID=seriesParams[0]
    #             chexiID=seriesParams[1]
    #             chexingID=specId
    #             specItem=(chexingID,pingpaiID,chexiID,specName,specLink)
    #             specList.append(specItem)
    #             self.log(specItem)
    #             # 保存车型到数据库
    #             self.count += 1
    #             self.log("saveCount：%d" % self.count)
    #             # yield specItem  #只有在scrapy.request方法中指定的方法才支持yield
    #     # 使用mysqlUtils将数据保存到数据库
    #     MySqlUtils.insertSpecItemList(specList)

    # def parseScoreAndPrice(self,response):
    #     #获取传递参数，车型对象
    #     specItem=response.meta['specItem']
    #     #解析评分
    #     scoreData = response.css(".koubei-data")
    #     score=0
    #     if scoreData:
    #         score = scoreData.xpath("span/a")[0].xpath("text()").extract_first()
    #         score = score[0:score.find("分")]
    #     #解析指导价
    #     priceData = response.css(".factoryprice")
    #     price=0
    #     if priceData:
    #         price = priceData.xpath("text()").extract_first()
    #         price=price.split("：")[1]
    #     specItem['money']=price
    #     specItem['score']=score
    #     self.log(specItem)
    #     #将车型信息保存到数据库
    #     yield specItem









