# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .mySqlUtils import MySqlUtils

class CiYunPipeline(object):

    # 所有车系车型元组集合
    totalChexingList=None




    def process_item(self, item, spider):
        return item



    def open_spider(self,spider):
        print("--------------------------------->openSpider")
        # 查询所有的车系车型集合[(chexingId,chexiID),(),,]
        CiYunPipeline.totalChexingList=MySqlUtils.querySpec()
        #



        pass


    def close_spider(self,spider):


        pass
