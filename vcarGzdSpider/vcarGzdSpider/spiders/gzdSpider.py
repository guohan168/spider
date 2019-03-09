
import scrapy, json,pymysql
from ..items import SpecItem
from ..mySqlUtils import MySqlUtils
import time
from ..pipelines import GzdPipeline

class GzdSpider(scrapy.Spider):
    name = "gzdSpider"
    urlModel = "https://carif.api.autohome.com.cn/Attention/LoadAttentionData.ashx?_callback=loadGuanZhuDuSpecSuccess&seriesids=%s"

    def start_requests(self):
        # 查询出所有的车系id
        #chexiIdSet=MySqlUtils.parseToChexiIdSet(MySqlUtils.querySeriesLink())
        urls = [
            "https://carif.api.autohome.com.cn/Attention/LoadAttentionData.ashx?_callback=loadGuanZhuDuSpecSuccess&seriesids=4012" #2660
        ]

        for chexiId in GzdPipeline.waitingCrawIdSet:
            url=self.urlModel % chexiId
            # url=urls[0]
            request=scrapy.Request(url=url, callback=self.parse)
            request.meta['chexiID']=chexiId
            # 统计已爬取车系id
            GzdPipeline.crawledChexiIdSet.add(chexiId)
            yield request



    #json示例
    """
            {
            "result": [{
                "specattentions": [{
                    "specid": 33409,
                    "attention": 12207658
                }, {
                    "specid": 33410,
                    "attention": 6040176
                }],
                "seriesid": 4171
            }],
            "returncode": 0,
            "message": ""
        }
    """

    def parse(self, response):
        chexiID=response.meta['chexiID']
        res=response.body_as_unicode()
        jsonStr=res[res.find("(")+1:res.find(")")]
        # 转json
        jsonObject=json.loads(jsonStr)
        result=jsonObject.get("result")
        if result:
            items=result[0]
            attentionList=items.get("specattentions")
            for attention in attentionList:
                specId=attention.get("specid")
                attentionValue=attention.get("attention")
                chexingItem=SpecItem()
                chexingItem['gzd']=attentionValue
                chexingItem['chexingID']=specId
                chexingItem['chexiID']=chexiID
                # 保存到数据库
                yield chexingItem



