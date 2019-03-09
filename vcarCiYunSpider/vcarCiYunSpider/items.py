# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CiYunItem(scrapy.Item):
    # 主键
    sid=scrapy.Field()
    # 车系id
    chexiID=scrapy.Field()
    # 车型id
    chexingID=scrapy.Field()
    # 评价分类：1 外观 2 内饰 3 舒适性 4 空间 5 动力 6 操控 7 油耗 8 性价比
    judgeType=scrapy.Field()
    # 词语
    words=scrapy.Field()
    # 参与评价人数
    judgeCount=scrapy.Field()
    # 词语情感类型, 有0为负面1为正面
    affectiveType=scrapy.Field()
    # 更新时间
    updateTime=scrapy.Field()





