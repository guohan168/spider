# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpecItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #品牌id
    pinpaiID=scrapy.Field()
    #车系id
    chexiID=scrapy.Field()
    # 车型id
    chexingID=scrapy.Field()
    #车型名称
    name=scrapy.Field()
    #车型url
    url=scrapy.Field()
    #车型指导价
    money=scrapy.Field()
    #车型评分
    score=scrapy.Field()
    #车型关注度
    gzd=scrapy.Field()
    #车型状态
    state=scrapy.Field()
    #sql操作标识，非车型数据库字段
    sqlType=scrapy.Field()



    def get_insert_sql(self):

        insert_sql="""
            INSERT INTO `vcar_vcyber_com`.`vcar_chexing`
                (`chexingID`,
                `pinpaiID`,
                `chexiID`,
                `name`,
                `url`)
                VALUES
                (
                %s,
                %s,
                %s,
                %s,
                %s
                );
        """
        params=(self['chexingID'],self['pinpaiID'],self['chexiID'],self['name'],self['url'])
        return insert_sql,params









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
    # 在售停售状态
    onSale=scrapy.Field()
    # 车系代表图片地址
    img=scrapy.Field()
    # 车系概要信息
    info=scrapy.Field()
    # 更新时间
    updateTime=scrapy.Field()
    #插入更新标识:1插入 2更新
    sqlType=scrapy.Field()

    # 更新车系信息：最小价格、最大价格、车系评分、级别
    def get_update_sql(self):
        update_sql = """
                    UPDATE `vcar_vcyber_com`.`vcar_chexi`
                    SET
                        `minMoney` = %s,
                        `maxMoney` = %s,
                        `score` = %s,
                        `jibie` = %s
                    WHERE `chexiID` = %s;
        """
        params = (self["minMoney"], self["maxMoney"], self["score"], self["jibie"], self["chexiID"])
        return update_sql, params

