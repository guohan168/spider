#coding=utf-8

import scrapy
from ..items import BrandItem
from ..mySqlUtils import MySqlUtils

class QuotesSpider(scrapy.Spider):
    #爬虫名称
    name = "brandSpider"
    #构造图片链接头
    https = "https:%s"
    #构造品牌链接
    brandLinkModel="https://car.autohome.com.cn/price/brand-%s.html"
    # 定义数据库中已经爬取的品牌id
    brandIdSet=set()
    # 爬取策略
    ruleId=1 # 1为只爬取有更新的 2为全部爬取全部更新


    #爬虫入口，请求品牌列表，爬取品牌数据
    def start_requests(self):
        # 查询已经存在于数据库中的品牌id
        res=MySqlUtils.queryBrandId()
        self.brandIdSet=MySqlUtils.parseBrandTupleListToBrandList(res)
        # self.log("===============================>")
        # self.log(res)
        urls = [
            "https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1&brandId=0&fctId=0&seriesId=0"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)




    #解析品牌数据
    def parse(self, response):
        # 提取数据
        body = response.xpath("//body")
        #brandSeriesLink = "https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1&brandId=%s&fctId=0&seriesId=0" #爬取车系链接

        letter=""
        for item in body.xpath("*"):
            if item.xpath("name()").extract_first() == "div":
                letter = item.xpath("text()").extract_first()
                continue
            li = item.xpath("li")
            for liData in li:
                brandItem=BrandItem()
                href = liData.xpath("h3/a/@href").extract_first()
                brandId = href[href.find("-") + 1:href.find(".")]
                brandName = liData.xpath("h3/a/text()").extract_first()
                brandLink=self.brandLinkModel % brandId
                brandItem['pingpaiID']=brandId
                brandItem['szm']=letter
                brandItem['name']=brandName
                brandItem['url']=brandLink
                #self.log(letter + "," + brandId + "," + brandName)
                # self.log("-------------------------------------->brandIdSet")
                # self.log(self.brandIdSet)
                # 如果数据库中已经存在该品牌ID则不进行爬取
                if self.ruleId == 1:
                    if brandId in self.brandIdSet:
                        continue
                # 接着爬取品牌图标
                request = scrapy.Request(url=brandLink, callback=self.parseBrandImg)
                request.meta['brandItem']=brandItem
                yield request




    #解析品牌图片logo的url
    def parseBrandImg(self,response):
        brandItem=response.meta['brandItem']
        brandImgUrl=response.css(".carbradn-pic").xpath("img/@src").extract_first()
        brandItem['imgUrl']=self.https % brandImgUrl
        #brandItem=(brandItem[0],brandItem[1],brandItem[2],self.https+brandImgUrl) #https是类变量，在构造函数中的为成员变量，都可以通过self来调用，也可以通过对象实例来调用
        self.log(brandItem)
        #保存到数据库
        yield brandItem





