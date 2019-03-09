# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import SeriesItem,SpecItem,DetailItem
from scrapy.conf import settings
import pymysql
import pymysql.cursors
import scrapy
import xlwt
import time,datetime
from twisted.enterprise import adbapi
from .mySqlUtils import MySqlUtils
import os,sys
from .point import Point


class DetailPipeline(object):
    count=0
    # 存放批量更新的数据集合
    updateItemList=list()
    # 断点续爬功能：记录写入到数据中的车型id串
    crawledIdSet=set()
    # 待爬取的车型id集合
    waitingCrawlIdSet=set()
    crawledIdStr=''
    # 断点文件路径
    pointFilePath=None
    overFilePath=None



    #通过构造函数设置属性
    def __init__(self,dbpool):
        self.dbpool=dbpool

    #初始化连接池
    @classmethod
    def from_settings(cls,settings):
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
        self.updateItemList.append((item['money'], item['score'], item['chexingID']))
        self.count += 1
        # 已爬车型id字符串后追加
        self.crawledIdStr += item['chexingID']+","
        self.crawledIdSet.add(item['chexingID'])
        if len(self.updateItemList) >= 100:
            # 执行数据库操作
            paramsList = self.updateItemList.copy()  # 因为是异步操作保存，所以要进行复制，否则清空后就没有数据了
            self.updateItemList.clear()
            self.dbpool.runInteraction(self.updateSpec, paramsList)
            # 向文件中写入已爬取的数据
            Point.savePoint(self.crawledIdStr)
            self.crawledIdStr=""
        return item



    def updateSpec(self,cursor,paramsList):
        print("update--------------------------------------->%s" % self.count)
        update_sql = """
                       UPDATE `vcar_vcyber_com`.`vcar_chexing`
                       SET
                           `money` = %s,
                           `score` = %s
                       WHERE `chexingID` = %s;
                   """
        try:
            cursor.executemany(update_sql, paramsList)

        except Exception as e:
            print(e)
            print(paramsList)
            self.errorCount += 1
            filename = "/Users/guohan/DeskTop/mySqlError.txt"
            error = self.errorModel % (self.errorCount, "piplines", "updateSpec(MoneyAndScore)", str(e))
            self.writeToFile(filename,error)

    # 写入文件
    def writeToFile(self,file,content):
        with open(file, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
            f.write(content)
            f.flush()
            f.close()

    def getTodayStr(self):
        return time.strftime('%Y-%m-%d', time.localtime(int(time.time())))

    def getYesterdayStr(self):
        yesterday=datetime.datetime.now() - datetime.timedelta(days=1)
        return time.strftime('%Y-%m-%d', yesterday.timetuple())

    # 生命周期爬虫启动时方法
    def open_spider(self, spider):
        # 从数据库中读取所有需要爬取的数据集
        res=MySqlUtils.querySpecLink()
        totalSpecIdSet=MySqlUtils.parseToSpecIdSet(res)
        # 初始化断点功能类
        Point.init()
        # 切入断点
        DetailPipeline.waitingCrawlIdSet=Point.cutInto(totalSpecIdSet)


    def close_spider(self, spider):

        # print(self.crawledIdStr)
        self.dbpool.runInteraction(self.updateSpec, self.updateItemList)
        # 向断点续爬文件中写入已爬车型id
        Point.savePoint(self.crawledIdStr)
        print("------------------------------------------------------------------------------------------> close")
        print("断点显示已爬取%s,剩余爬取%s" % (self.count,len(DetailPipeline.waitingCrawlIdSet)-self.count))
        # 如果正常爬取结束，则在temp目录下写入over.txt 标识文件
        if len(DetailPipeline.waitingCrawlIdSet) >= self.count:
            Point.complete()

