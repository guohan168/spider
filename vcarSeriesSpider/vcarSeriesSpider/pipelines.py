# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymysql
import pymysql.cursors
import scrapy
import xlwt
from twisted.enterprise import adbapi
from scrapy import log
from .mySqlUtils import MySqlUtils
from .point import Point

class SeriesPipeLine(object):

    # 定义已爬取车系id集合
    chexiIdSet=None
    # 待爬取品牌id集合
    waitingCrawlBrandIdSet=None
    # 已爬取品牌ID集合
    crawledBrandIdSet=set()
    # 爬取计数器
    count=0
    # 更新计数器
    updateCount=0

    #添加连接池属性,通过构造方法将已经初始化过的连接池传入
    def __init__(self,dbpool):
        self.dbpool=dbpool
        self.chexiIdSet=MySqlUtils.parseToChexiIdSet(MySqlUtils.querySeries())

    #初始化连接池,该方法生命周期初始化方法
    @classmethod
    def from_settings(cls,settings):
        dbpool=adbapi.ConnectionPool("pymysql",
                                     host=settings["MYSQL_HOST"],
                                     db=settings["MYSQL_DB"],
                                     user=settings["MYSQL_USER"],
                                     password=settings["MYSQL_PASSWORD"],
                                     charset=settings["CHARSET"],
                                     cursorclass=pymysql.cursors.DictCursor,
                                     use_unicode=True)
        return cls(dbpool)


    def process_item(self, item, spider):
        # 将品牌id存入已爬取的品牌id集合中，用于断点控制
        self.crawledBrandIdSet.add(item['pinpaiID'])
        #通过item的sqlType来判断做更新还是插入操作，当sqlType等于1时做插入操作，等于2时做更新操作
        sqlType=item['sqlType']
        # 如果数据库中存在chexiID则更新，否则插入
        if item['chexiID'] in self.chexiIdSet:
            self.dbpool.runInteraction(self.do_update,item)
        else:
            self.dbpool.runInteraction(self.do_insert, item)


    #执行具体的插入操作
    def do_insert(self,cursor,item):
        insert_sql,params=item.get_insert_sql()
        cursor.execute(insert_sql,params)


    # 更新chexiid、pingpaiId、name、url、chexiType
    def do_update(self,cursor,item):
        params,update_sql=item.get_update_sql()
        cursor.execute(update_sql,params)

    def open_spider(self, spider):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>openSpider")
        # 车系根据品牌id来爬，故查出所有的品牌id
        res = MySqlUtils.queryBrandId()
        idSet = MySqlUtils.parseToIdSet(res)
        # 初始化断点功能类
        Point.init()
        # 切入断点
        SeriesPipeLine.waitingCrawlBrandIdSet = Point.cutInto(idSet)
        print(SeriesPipeLine.waitingCrawlBrandIdSet)


    def close_spider(self,spider):
        # 向断点续爬文件中写入已爬车型id
        crawledIdStr=""
        for id in SeriesPipeLine.crawledBrandIdSet:
            crawledIdStr += id + ","
        Point.savePoint(crawledIdStr)
        print("------------------------------------------------------------------------------------------> close")
        print("断点显示已爬取%s,剩余爬取%s，新增%s" % (SeriesPipeLine.count, len(SeriesPipeLine.waitingCrawlBrandIdSet) - SeriesPipeLine.count,SeriesPipeLine.updateCount))
        # 如果正常爬取结束，则在temp目录下写入over.txt 标识文件
        if len(SeriesPipeLine.waitingCrawlBrandIdSet) <= SeriesPipeLine.count:
            Point.complete()


