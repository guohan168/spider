# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpecItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 品牌id
    pinpaiID = scrapy.Field()
    # 车系id
    chexiID = scrapy.Field()
    # 车型id
    chexingID = scrapy.Field()
    # 车型名称
    name = scrapy.Field()
    # 车型url
    url = scrapy.Field()
    # 车型指导价
    money = scrapy.Field()
    # 车型评分
    score = scrapy.Field()
    # 车型关注度
    gzd = scrapy.Field()
    # 车型状态
    state = scrapy.Field()
    # sql操作标识，非车型数据库字段
    sqlType = scrapy.Field()

    def get_update_sql(self):
        update_sql = """
                        UPDATE `vcar_vcyber_com`.`vcar_chexing`
                        SET
                        `gzd` = %s
                        WHERE `chexingID` = %s;
                     """
        #params = (self['gzd'], self['chexingID'])
        return update_sql
