

import scrapy,re
from ..mySqlUtils import MySqlUtils
from ..items import SeriesItem
from ..pipelines import SeriesPipeLine
import datetime


class seriesSpider(scrapy.Spider):

    name = "seriesSpider"
    seriesTreeLinkModel="https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1&brandId=%s&fctId=0&seriesId=0"
    seriesLinkModel="https://car.autohome.com.cn%s"

    # 已爬取车系id集合
    seriesIdSet=None
    # 爬取规则
    ruleId=2  # 1为数据库中已存在的则不保存，2是全部更新

    #爬虫入口
    def start_requests(self):
        # 初始化已爬取车系id集合
        self.seriesIdSet=MySqlUtils.parseToChexiIdSet(MySqlUtils.querySeries())

        # 请求查询车系信息
        # res=MySqlUtils.queryBrandId()
        # 从断点文件中获取剩余未爬的品牌ID集合
        res=SeriesPipeLine.waitingCrawlBrandIdSet
        #res是元组的列表集合，每个元组只包含一个元素即品牌id
        for brandId in res:

            #self.log(brandId[0])
            #self.log(type(brandId[0]))
            request=scrapy.Request(url=self.seriesTreeLinkModel % brandId, callback=self.parse)
            request.meta['brandId']=brandId

            # 记录已爬品牌ID
            SeriesPipeLine.crawledBrandIdSet.add(brandId)
            SeriesPipeLine.count += 1

            yield request


    #解析查询结果
    def parse(self, response):
        #获取绑定参数
        brandId=response.meta['brandId']
        #车系数据在dl标签下，dl标签中并列dt和dd，dt为子品牌信息，dd为车系信息，因此需要获取dl标签下的子元素集
        seriesItems = response.xpath("//dl/*")
        self.log(seriesItems)
        brandSubId=0
        brandSubName=""
        for itemData in seriesItems:
            #数据封装对象
            item=SeriesItem()
            #取出子品牌，子品牌id，车系id，车系名称，车系url，车系车型数量，是否停售
            #通过取出当前标签的名称判断当前标签是否属于子品牌
            if(itemData.xpath("name()").extract_first() == "dt"):
                #获取子品牌名称
                brandSubName=itemData.xpath("a/text()").extract_first().strip()

                #通过brandSubHref获取brandSubId:
                #brandSubHref=item.xpath("a/@href").extract_first() #/price/brand-15-29.html 29为其brandSubId,需要截取获得
                #brandSubId=brandSubHref[brandSubHref.rfind("-")+1:brandSubHref.find(".")]

                #将取出的值用于下面的车系，表示该车系属于某一个子品牌下的
                continue
            #取出车系信息
            seriesName=itemData.xpath("a/text()").extract_first().strip()
            #取出车系链接/price/series-66.html
            seriesHref=itemData.xpath("a/@href").extract_first()
            #截取车系id
            seriesId=seriesHref[seriesHref.find("-")+1:seriesHref.find(".")]
            #获取车型数量
            seriesMarks=itemData.xpath("a/em/text()").extract_first()
            seriesNumSearch=re.search(r'\d+',str(seriesMarks))
            seriesNum=0
            if(seriesNumSearch):
                seriesNum =seriesNumSearch.group()

            #获取是否停售
            seriesMark='1'
            if(re.search(r'停售',str(seriesMarks))):
                seriesMark='0'
            seriesTuple=(seriesId,brandId,brandSubName,seriesName,self.seriesLinkModel % seriesHref)
            item['chexiID']=seriesId
            item['pinpaiID']=brandId
            item['chexiType']=brandSubName
            item['name']=seriesName
            item['url']=self.seriesLinkModel % seriesHref
            item['onSale']=seriesMark
            item['updateTime']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['sqlType']='1'
            self.log(seriesTuple)
            # 记录新爬取到的车系
            if seriesId not in self.seriesIdSet:
                SeriesPipeLine.updateCount += 1
            #保存到数据库
            if self.ruleId == 1:
                if seriesId in self.seriesIdSet:
                    continue

            yield item


        #保存到数据库
        #self.saveToMySql(seriesLinkList)





