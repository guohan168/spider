# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import ScoreItem
from .mySqlUtils import MySqlUtils

class ScorePipeline(object):
    # 所有的车型id集合
    chexingIdSet=None
    # 存放枚举
    enumDict=None

    def process_item(self, item, spider):
        return item





    def open_spider(self,spider):
        print("------------------open")
        # 初始化车型id集合
        res=MySqlUtils.querySpec()
        ScorePipeline.chexingIdSet=MySqlUtils.parseToChexingIdSet(res)
        print(len(ScorePipeline.chexingIdSet))
        # 初始化枚举
        enumRes=MySqlUtils.queryEnum('qczj_score')
        ScorePipeline.enumDict=MySqlUtils.parseEnum(enumRes)




    def close_spider(self,spider):


        pass
