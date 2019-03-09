import scrapy,pymysql,re,time,requests,datetime,random
from ..mySqlUtils import MySqlUtils
from ..addressUtils import AddressUtils
from ..items import DealerItem

class DealerSpider(scrapy.Spider):


    name = "dealerSpider"
    url="https://dealer.autohome.com.cn/china/0/0/0/0/%s/1/0/0.html"

    def __init__(self):
        # 初始化品牌品牌id字典
        brandRes=MySqlUtils.query(MySqlUtils.sql_query_brand)
        self.brandDict=MySqlUtils.parseToDict(brandRes,1,0)
        print(self.brandDict)




    def start_requests(self):
        # 请求
        for i in range(1,1722):
            time.sleep(0.5)
            url=self.url % i
            request=scrapy.Request(url=url,callback=self.parse)
            yield request



    # 解析
    def parse(self, response):
        listItem=response.css(".list-item")
        for li in listItem:
            # 解析经销商名称
            imgUrl=li.css(".img-box img ::attr(src)").extract_first()
            infoLiList=li.css(".info-wrap li")
            item=DealerItem()
            for i,infoLi in enumerate(infoLiList):
                if i == 0:
                    # 解析经销商id
                    dealerLink=infoLi.css("a ::attr(href)").extract_first()
                    dealerLink=dealerLink[:dealerLink.rfind("#")]
                    dealerId=re.search(r'\d+',dealerLink).group()
                    # 解析经销商名称
                    dealerName=infoLi.css("a span ::text").extract_first()
                    # 解析经销商类型
                    spanList=infoLi.css("span")
                    dealerType=spanList[1].css(" ::text").extract_first()
                    # 解析徽章
                    huizhang=infoLi.css(".icon-medal i ::attr(class)").extract_first()
                    if huizhang:
                        huizhang=huizhang[huizhang.rfind("-")+1:]
                    item['homepageUrl']=dealerLink
                    item['sid']=dealerId
                    item['dealerName']=dealerName
                    item['type']=dealerType
                    item['badge']=huizhang
                # 解析主营品牌和在售车型数量
                if i == 1:
                    # 解析主营品牌
                    mainBrand=infoLi.css("span em ::text").extract_first()
                    # 反向获取品牌id
                    mainBrandId=None
                    for brandName in self.brandDict.keys():
                        if mainBrand in brandName:
                            mainBrandId=self.brandDict.get(brandName)
                            break
                    onSaleText=infoLi.css("a ::text").extract_first()
                    # 解析在售车型数量
                    onSaleNum=re.search(r'\d+',onSaleText).group()
                    item['mainBrand']=mainBrand
                    item['mainBrandId']=mainBrandId
                    item['onSaleNum']=onSaleNum
                # 解析电话、销售范围、销售范围明细
                if i == 2:
                    # 解析电话
                    tel=infoLi.css(".tel ::text").extract_first()
                    # 解析销售范围
                    limitAreaType=infoLi.css(".gray.data-business-tip ::text").extract_first()
                    # 解析销售范围明细
                    limitAreaDetail=infoLi.css(".floating ::text").extract_first()
                    item['tel']=tel
                    item['limitAreaType']=limitAreaType
                    item['limitAreaDetail']=limitAreaDetail

                # 解析地址
                if i == 3:
                    addr=infoLi.css(".info-addr ::text").extract_first()
                    # 将地址解析成省市县及详细地址
                    pro_name,pro_code,city_name,city_code,county_name,county_code=AddressUtils.parseProvinceCityCount(title=item['dealerName'],content=addr)
                    item['provinceCode']=pro_code
                    item['province']=pro_name
                    item['cityCode']=city_code
                    item['city']=city_name
                    item['countyCode']=county_code
                    item['county']=county_name
                    item['detailAddr']=addr
            # 保存到数据库
            item['headImgUrl']=imgUrl
            yield item








