# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 车系
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
                        `img` = %s
                    WHERE `chexiID` = %s;
        """
        params = (self['img'],self['chexiID'])
        return update_sql, params


# 保值率
class KeepValue(scrapy.Item):

    # 主键
    sid=scrapy.Field()
    # 车系id
    chexiID=scrapy.Field()
    # 年份
    year=scrapy.Field()
    # 保值率
    keepValue=scrapy.Field()
    # 修改时间
    updateTime=scrapy.Field()

    # 插入数据
    def get_insert_sql(self):
        sql="""
                INSERT INTO `vcar_vcyber_com`.`vcar_qczj_keep_value`
                    (`sid`,
                    `chexiID`,
                    `year`,
                    `keepValue`)
                    VALUES
                    (%s,
                    %s,
                    %s,
                    %s);
        """
        params=(self['sid'],self['chexiID'],self['year'],self['keepValue'])
        return sql,params

    # 更新
    def get_update_sql(self):
        sql="""
                UPDATE `vcar_vcyber_com`.`vcar_qczj_keep_value`
                SET
                    `year` = %s,
                    `keepValue` = %s,
                    `updateTime` = %s
                WHERE `chexiID` = %s and year=%s;
        """
        params=(self['year'],self['keepValue'],self['updateTime'],self['chexiID'],self['year'])
        return sql,params

