# -*- coding: utf-8 -*-
from scrapy.conf import settings
import pymysql
import pymysql.cursors
import scrapy
import xlwt
from twisted.enterprise import adbapi
from scrapy import log
from .mySqlUtils import MySqlUtils
from .point import Point

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#转换编码类
class EncodePipeline(object):
    #编码转换
    def process_item(self,item,spider):
        for k in item:
            item[k]=item[k].encode("utf8")
        return item




#保存数据库
class SavePipeline(object):
    brandIdSet=None
    # 等待被爬取的品牌集合
    waitingCrawlIdSet=None
    # 已爬取的id字符串集合
    crawledIdStr=""
    # 爬取计数
    count=0


    # 连接数据库
    def __init__(self,dbpool):
        #初始化数据库连接池
        self.dppool=dbpool
        res=MySqlUtils.queryBrandId()
        self.brandIdSet=MySqlUtils.parseBrandTupleListToBrandList(res)
        #获取数据库连接
        #host=settings['MySqlHost']
        #port=settings['MySqlPort']
        #dbName=settings['MySqlDbName']
        #client =

    @classmethod
    def from_settings(cls,settings):
        dbpool=adbapi.ConnectionPool("pymysql",
                                     host=settings["MYSQL_HOST"],
                                     db=settings["MYSQL_DB"],
                                     user=settings["MYSQL_USER"],
                                     password=settings["MYSQL_PASSWORD"],
                                     charset=settings["CHARSET"],
                                     cursorclass=pymysql.cursors.DictCursor,
                                     use_unicode=True
                                     )
        return cls(dbpool)

    def process_item(self, item, spider):
        self.count+=1
        # 判断品牌id是否已经存在于品牌表中,若存在则更新，否则则插入
        self.crawledIdStr+=item['pingpaiID']+","
        if item['pingpaiID'] in self.brandIdSet:
            self.dppool.runInteraction(self.do_update, item)
        else :
            self.dppool.runInteraction(self.do_insert,item)


    #执行具体插入
    def do_insert(self,cursor,item):
        #根据不同的item，构建不同的sql语句并插入到mysql中
        insert_sql,params=item.get_insert_sql()
        cursor.execute(insert_sql,params)

    # 向数据库中更新数据
    def do_update(self,cursor,item):
        update_sql,params=item.get_update_sql()
        i=cursor.execute(update_sql,params)

    #   开启爬虫生命周期方法
    def open_spider(self,spider):
        pass

    def close_spider(self,spider):
       pass










