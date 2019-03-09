# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DealerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sid=scrapy.Field()
    dealerName=scrapy.Field()
    homepageUrl=scrapy.Field()
    headImgUrl=scrapy.Field()
    provinceCode=scrapy.Field()
    province=scrapy.Field()
    cityCode=scrapy.Field()
    city=scrapy.Field()
    county=scrapy.Field()
    countyCode=scrapy.Field()
    mainBrand=scrapy.Field()
    mainBrandId=scrapy.Field()
    tel=scrapy.Field()
    mobile=scrapy.Field()
    detailAddr=scrapy.Field()
    onSaleNum=scrapy.Field()
    type=scrapy.Field()
    badge=scrapy.Field()
    limitAreaType=scrapy.Field()
    limitAreaDetail=scrapy.Field()
    status=scrapy.Field()
    updateTime=scrapy.Field()



