# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import SpecItem
from scrapy.conf import settings
import pymysql
import pymysql.cursors
import scrapy
import xlwt
from twisted.enterprise import adbapi
from scrapy import log
from .mySqlUtils import MySqlUtils
from .point import Point


class GzdPipeline(object):
    count = 0
    chexiID=None
    itmeList=list()

    # 已爬车系集合
    crawledChexiIdSet=set()
    # 待爬车系ID集合
    waitingCrawIdSet=None


    # 通过构造函数设置属性
    def __init__(self, dbpool):
        self.dbpool = dbpool


    # 初始化连接池
    @classmethod
    def from_settings(cls, settings):
        dbpool = adbapi.ConnectionPool("pymysql",
                                       host=settings["MYSQL_HOST"],
                                       db=settings["MYSQL_DB"],
                                       user=settings["MYSQL_USER"],
                                       password=settings["MYSQL_PASSWORD"],
                                       charset=settings["CHARSET"],
                                       cursorclass=pymysql.cursors.DictCursor,
                                       use_unicode=True)

        return cls(dbpool)

    def process_item(self, item, spider):
        self.count += 1
        self.itmeList.append((item['gzd'], item['chexingID']))
        if len(self.itmeList) >= 100:
            # 执行数据库操作
            paramsList=self.itmeList.copy()
            self.itmeList.clear()
            self.dbpool.runInteraction(self.updateGzdList,paramsList)
        return item






    def updateGzdList(self,cursor,paramsList):
        print("-------------->execute update %s" % self.count)
        update_sql = """
                               UPDATE `vcar_vcyber_com`.`vcar_chexing`
                               SET
                               `gzd` = %s
                               WHERE `chexingID` = %s;
                     """
        try:
            cursor.executemany(update_sql, paramsList)

        except Exception as e:
            pass


    def open_spider(self,spider):
        # 查询车系id集合
        res=MySqlUtils.querySeriesLink()
        totalChexiIdSet=MySqlUtils.parseToChexiIdSet(res)
        # 初始化断点
        Point.init()
        # 切入断点爬取
        GzdPipeline.waitingCrawIdSet=Point.cutInto(totalChexiIdSet)


    def close_spider(self,spider):
        print("------------> close,save:%s" % self.count)
        self.dbpool.runInteraction(self.updateGzdList,self.itmeList)
        # 保存断点
        crawledIdStr=""
        for id in GzdPipeline.crawledChexiIdSet:
            crawledIdStr += id + ","
        Point.savePoint(crawledIdStr)
        if len(GzdPipeline.waitingCrawIdSet) == len(GzdPipeline.crawledChexiIdSet):
            Point.complete()
        print("断点显示已爬取%s,剩余爬取%s" % (len(GzdPipeline.crawledChexiIdSet),len(GzdPipeline.waitingCrawIdSet) - len(GzdPipeline.crawledChexiIdSet)))

        spider.close('gzdSpider','completed')




