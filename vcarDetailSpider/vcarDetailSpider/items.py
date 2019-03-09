# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DetailItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass





class SpecItem(scrapy.Item):
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

    #更新车型指导价和用户评分
    def updateMoneyAndScoreSql(self):
        updateSql="""
                    UPDATE `vcar_vcyber_com`.`vcar_chexing`
                    SET
                        `money` = %s,
                        `score` = %s
                    WHERE `chexingID` = %s;
        """
        params=(self['money'],self['score'],self['chexingID'])
        return updateSql,params



class SeriesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #车系id
    chexiID=scrapy.Field()
    #品牌id
    pinpaiID=scrapy.Field()
    #车系类别，相当于子品牌
    chexiType=scrapy.Field()
    #车系名称
    name=scrapy.Field()
    #车系对应的车系及车型列表页链接
    url=scrapy.Field()
    #该车系最小售价
    minMoney=scrapy.Field()
    #该车系最大售价
    maxMoney=scrapy.Field()
    #该车系用户平均评分
    score=scrapy.Field()
    #按大小将车分为不同级别，如紧凑型，微型、小型、中型、大型、SUV，mpv、皮卡等
    jibie=scrapy.Field()
    #插入更新标识:1插入 2更新
    sqlType=scrapy.Field()

    #插入从车系列表页爬取的车系类别、车系ID、车系名称、车系url
    def get_insert_sql(self):
        insert_sql="""      
                    INSERT INTO `vcar_vcyber_com`.`vcar_chexi`
                        (`chexiID`,
                        `pinpaiID`,
                        `chexiType`,
                        `name`,
                        `url`)
                        VALUES(
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                        );                
        """
        params=(self['chexiID'],self['pinpaiID'],self['chexiType'],self['name'],self['url'])
        return insert_sql,params




