

import scrapy,random,re
from ..pipelines import ScorePipeline
from ..items import ScoreItem

class  ScoreSpider(scrapy.Spider):
    # 爬虫名称
    name = "scoreSpider"
    # 爬取链接,占位符为车型id
    kouBeiUrl="https://k.autohome.com.cn/spec/%s"

    def start_requests(self):
        self.log("===================>start")
        self.log(len(ScorePipeline.chexingIdSet))
        for chexingId in ScorePipeline.chexingIdSet:
            request=scrapy.Request(url=self.kouBeiUrl % chexingId,callback=self.parse)
            request.meta['chexingId']=chexingId
            yield request



    def parse(self, response):
        chexingId=response.meta['chexingId']
        ulArr = response.css(".date-ul.fn-left")
        self.log("1111111111111111111111--->type(ulArr)")
        self.log(len(ulArr))
        for ul in ulArr:
            for i,li in enumerate(ul.css("li")):
                if i == 0:
                    continue
                # 取出当前类别值
                optionName=li.css(".width-01 ::text").extract_first()
                optionName=optionName.rstrip()
                optionName=optionName.lstrip()

                # 取出当前类别的评分
                optionValue=li.css(".width-02 ::text").extract_first()
                optionValue=optionValue.rstrip()
                optionValue=optionValue.lstrip()
                if optionValue == "-":
                    optionValue == None

                # 取出当前类别的高于／低于
                # 取值
                cpValue = li.css(".width-03").xpath("string(.)").extract_first()
                cpValue = cpValue.rstrip()
                cpValue = cpValue.lstrip()
                cpValue = re.search(r'\d+(\.\d+)?',cpValue)
                if cpValue:
                    cpValue=cpValue.group()
                # 判断是否存在子元素i
                if li.css(".width-03 i"):
                    # 根据css名称 判断高于低于
                    cssClassName = li.css(".width-03 i::attr(class)").extract_first()
                    pcssName, subCssName = cssClassName.split(" ")
                    if subCssName == 'icon-dy':
                        cpValue = -1 * float(cpValue)

                item=ScoreItem()
                item['sid']=chexingId+"_"+str(random.randint(100000,999999))
                item['chexingID']=chexingId
                item['scoreType']=ScorePipeline.enumDict[optionName]
                item['score']=optionValue
                item['cpScore']=cpValue

                yield item



