
import scrapy,pymysql,re,json,random,datetime
from ..pipelines import SeriesExtPipeline
from ..items import SeriesItem,KeepValue
class SeriesSpider(scrapy.Spider):
    # 爬虫名称
    name = "seriesExtSpider"
    # 保值率链接地址,%s为车系ID
    keepValueUrlModel="https://pinguapi.che168.com/v1/assesspublic/seriesofrate?_appid=m.m&seriesid=%s&levelid=3&markvalue=&callback=seriesKeepValueCallback"
    # 车系代表图片爬取链接地址,%s为车系id
    seriesImgUrlModel="https://www.autohome.com.cn/%s"
    # 停售车系图片地址:第一个占位符代表车型id，第二个为网页id，均可以从当前页获取到
    noSailSeriesImgUrl="https://car.autohome.com.cn/photo/series/%s/1/%s.html"

    # 设置爬取规则：当ruleID为1时，只爬取img及保值率为空的车系
    ruleId=1

    count=0


    def start_requests(self):
        for chexiId in SeriesExtPipeline.waitingCrawlIdSet:
            # 断点计数器，统计请求次数及哪些车系id
            SeriesExtPipeline.crawledIdSet.add(chexiId)
            # 当ruleId等于1时，只爬取车系表中img为空的车系,当ruleId等于2时，更新全部
            if self.ruleId == 1:
                # 无值才爬，否则不爬
                if chexiId not in SeriesExtPipeline.savedImgIdSet:

                    # 爬取车系图片
                    imgUrl = self.seriesImgUrlModel % chexiId
                    imgRequest = scrapy.Request(url=imgUrl, callback=self.parseImg)
                    imgRequest.meta['chexiID'] = chexiId
                    yield imgRequest
                else:
                    continue

                # 无值才爬，否则不爬
                if chexiId not in SeriesExtPipeline.savedChexiIdSet:
                    # 爬取保值率
                    keepValueUrl = self.keepValueUrlModel % chexiId
                    keepValueRequest = scrapy.Request(url=keepValueUrl, callback=self.parseKeepValue)
                    keepValueRequest.meta['chexiID'] = chexiId
                    yield keepValueRequest
                else:
                    continue
            elif self.ruleId == 2:
                # 爬取车系图片
                imgUrl = self.seriesImgUrlModel % chexiId
                imgRequest = scrapy.Request(url=imgUrl, callback=self.parseImg)
                imgRequest.meta['chexiID'] = chexiId
                yield imgRequest

                keepValueUrl = self.keepValueUrlModel % chexiId
                keepValueRequest = scrapy.Request(url=keepValueUrl, callback=self.parseKeepValue)
                keepValueRequest.meta['chexiID'] = chexiId
                yield keepValueRequest






    # 解析图片
    def parseImg(self, response):

        chexiID=response.meta['chexiID']
        imgSrc = response.css(".pic-main img::attr(src)").extract_first()

        # 如果存在，则为在售车系，否则为停售车系
        if imgSrc:

            imgSrc=imgSrc.replace('380x285','760x570')
            item=SeriesItem()
            item['chexiID']=chexiID
            item['img']="https:%s" % imgSrc
            yield item
        else:
            # //car.autohome.com.cn/photo/series/12423/1/1727122.html
            # href = response.css(".piclist a::attr(href)").extract_first() #部分车系取不到，因此不能通过此方法直接获取图片链接
            # //car.autohome.com.cn/photolist/series/3382/1408569.html?pvareaid=101468
            href = response.css(".models_pics a::attr(href)").extract_first()
            #缩略小图
            smallImg=response.css(".models_pics img::attr(src)").extract_first()
            if href:

                # 取出车型id
                chexingId=re.search(r'\d+',href).group()
                # 取出html的Id
                htmlId=href[href.rfind("/")+1:href.rfind(".")]
                # 请求图片所在的网址
                request=scrapy.Request(url=self.noSailSeriesImgUrl % (chexingId,htmlId),callback=self.parseNoSailImg,dont_filter=True)
                request.meta['chexiID']=chexiID
                request.meta['smallImg']=smallImg

                yield request


    # 解析停售车系图片
    def parseNoSailImg(self,response):
        chexiID=response.meta['chexiID']
        smallImg=response.meta['smallImg']
        # 取出图片地址
        src = response.css("#img ::attr(src)").extract_first()
        item = SeriesItem()
        item['chexiID'] = chexiID
        if src:
            item['img']="https:%s" % src
        else:
            item['img']=smallImg
        yield item




    # 解析保值率
    def parseKeepValue(self,response):
        chexiID = response.meta['chexiID']
        res = response.body_as_unicode()
        jsonStr = res[res.find("(") + 1:res.find(")")]
        # 转json
        jsonObject = json.loads(jsonStr)
        result = jsonObject.get("result")
        if result:
            for item in result:
                keepValueItem = KeepValue()
                keepValueItem['year'] = item['year']
                keepValueItem['keepValue'] = item['keeprate']
                keepValueItem['chexiID']=chexiID
                # 如果表中已存在则更新，否则插入
                if chexiID not in SeriesExtPipeline.savedChexiIdSet:
                    keepValueItem['sid']=chexiID+"_"+str(item['year'])+"_"+str(random.randint(1000000,9999999))
                    yield keepValueItem
                else:
                    keepValueItem['updateTime']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    yield keepValueItem


        yield keepValueItem





