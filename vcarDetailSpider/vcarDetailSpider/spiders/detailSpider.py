import scrapy,pymysql,re
from ..items import DetailItem,SpecItem
from ..mySqlUtils import MySqlUtils
from ..pipelines import DetailPipeline


class DetailSpider(scrapy.Spider):

    # 请求计数器
    count=0


    name = "detailSpider"
    https = "https:%s"
    host = "https://car.autohome.com.cn%s"
    configLinkModel="https://car.autohome.com.cn/config/spec/%s.html"
    detailLinkModel="https://www.autohome.com.cn/spec/%s"


    #读取车型数据，请求车型详情页链接
    def start_requests(self):
        #读取数据库车型表，获取车型链接
        specList=MySqlUtils.querySpecLink()
        for chexingId in DetailPipeline.waitingCrawlIdSet:
            #self.log(item[4])
            request=scrapy.Request(url=self.detailLinkModel % chexingId,callback=self.parse)
            request.meta['chexingId']=chexingId
            yield request

    #解析车型详情页指导价、评分、车型配置链接
    def  parse(self, response):
        chexingId=response.meta['chexingId']
        specItem=SpecItem()
        #解析指导价
        price=0
        priceDes=response.css(".factoryprice::text").extract_first() #'厂商指导价：3.58'
        priceGroup=re.search(r'\d+(\.\d+)*',priceDes)
        if priceGroup:
            price=priceGroup.group()
        #解析评分
        score=0
        scoreData=response.css(".scroe")
        if scoreData:
            scoreDes=scoreData.xpath("text()").extract_first()
            scoreDesGroup=re.search(r'\d+(\.\d+)*', scoreDes)
            if scoreDes:
                score=scoreDesGroup.group()
        #解析配置链接
        configLink=self.configLinkModel % chexingId
        self.log((price,score,configLink))
        #更新车型表评分和指导价
        specItem['money']=price
        specItem['score']=score
        specItem['chexingID']=chexingId
        specItem['sqlType']='2'
        self.count+=1
        yield specItem

        #请求配置链接




    #解析配置页面
    def parseDetail(self):
        pass





