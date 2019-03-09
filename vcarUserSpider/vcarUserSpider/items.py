# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sid=scrapy.Field()
    headImg=scrapy.Field()
    sex=scrapy.Field()
    province=scrapy.Field()
    provinceCode=scrapy.Field()
    city=scrapy.Field()
    cityCode=scrapy.Field()
    level=scrapy.Field()
    focusNum=scrapy.Field()
    fansNum=scrapy.Field()
    vStatus=scrapy.Field()
    updateTime=scrapy.Field()

