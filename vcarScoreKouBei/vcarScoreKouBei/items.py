# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 主键
    sid = scrapy.Field()
    # 车型id
    chexingID=scrapy.Field()
    # 分数类型
    scoreType = scrapy.Field()
    # 分数
    score=scrapy.Field()
    # 与同级别相比较高于或低于，低于用负数表示
    cpScore=scrapy.Field()
    # 更新时间
    updateTime=scrapy.Field()


