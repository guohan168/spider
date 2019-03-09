# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 爬取过来的数据包括车系图片和保值率两个对象，可采用两个pipeline进行保存操作
from .mySqlUtils import MySqlUtils
from .items import SeriesItem,KeepValue
import pymysql
import pymysql.cursors
import scrapy
import xlwt
import time,datetime
from twisted.enterprise import adbapi
from .mySqlUtils import MySqlUtils
from .point import Point

class SeriesExtPipeline(object):
    # 车系id集合
    chexiIdSet=None
    # 存放img的item集合
    imgItemList=list()
    # 存放插入到保值率表中的item集合
    insertKeepValueItemList=list()
    # 存放更新到保值率表中的item集合
    updateKeepValueItemList=list()
    # 已爬取保值率的车系id
    savedChexiIdSet=None
    # 已爬取车系图片的车系id集合,即车系表中img不为空的车系id集合
    savedImgIdSet=None
    # 断点用待爬车系
    waitingCrawlIdSet=None

    # img更新计数器
    imgUpdateCount=0
    # 保值率插入计数器
    keepValueInsertCount=0
    # 保值率更新计数器
    keepValueUpdateCount=0
    # 断点用已爬取的车系id集合
    crawledIdSet=set()




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
        # 更新图片
        if isinstance(item,SeriesItem):
            self.imgUpdateCount += 1
            # 采用异步批量写入数据库
            self.imgItemList.append((item['img'],item['chexiID']))
            # 如果大于100则进行批量保存
            if len(self.imgItemList) >= 100:
                imgItemListCopy=self.imgItemList.copy()
                self.imgItemList.clear()
                # 保存到数据库
                self.dbpool.runInteraction(self.update_img,imgItemListCopy)
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>更新图片%s" % self.imgUpdateCount)

        # 更新保值率
        else:
            # 如果保值率表中不存在则插入，否则更新
            if item['chexiID'] not in SeriesExtPipeline.savedChexiIdSet:
                self.keepValueInsertCount += 1
                self.insertKeepValueItemList.append((item['sid'],item['chexiID'],item['year'],item['keepValue']))
                if len(self.insertKeepValueItemList) >= 100 :
                    insertCopyList=self.insertKeepValueItemList.copy()
                    self.insertKeepValueItemList.clear()
                    self.dbpool.runInteraction(self.insert_keepvalue,insertCopyList)
                    print("------------------------------------------------->保存保值率：%s" % self.keepValueInsertCount)
            else:
                self.keepValueUpdateCount += 1
                self.updateKeepValueItemList.append((item['year'],item['keepValue'],item['updateTime'],item['chexiID'],item['year']))
                if len(self.updateKeepValueItemList) >= 100:
                    updateCopyList=self.updateKeepValueItemList.copy()
                    self.updateKeepValueItemList.clear()
                    self.dbpool.runInteraction(self.update_keepValue,updateCopyList)
                    print("=================================================>更新保值率：%s" % self.keepValueUpdateCount)



    # 批量更新车系图片
    def update_img(self,cursor,params):
        update_sql="""
                    UPDATE `vcar_vcyber_com`.`vcar_chexi`
                    SET
                        `img` = %s
                    WHERE `chexiID` = %s;
        """
        try:
            cursor.executemany(update_sql,params)
        except Exception as e:
            print(e)
            pass

    # 批量插入保值率
    def insert_keepvalue(self,cursor,params):
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
        try:
            cursor.executemany(sql,params)
        except Exception as e:
            print(e)
            pass


    # 批量更新保值率
    def update_keepValue(self,cursor,params):
        sql="""
                UPDATE `vcar_vcyber_com`.`vcar_qczj_keep_value`
                SET
                    `year` = %s,
                    `keepValue` = %s,
                    `updateTime` = %s
                WHERE `chexiID` = %s and year=%s;
        """
        try:
            cursor.executemany(sql,params)
        except Exception as e:
            print(e)
            pass





    def open_spider(self,spider):
        # 初始化相关变量的值
        res=MySqlUtils.querySeries()
        SeriesExtPipeline.chexiIdSet=MySqlUtils.parseToIdSet(res)
        # 初始化已爬取过保值率的车系id,用于判重，并决定是否爬取或则做插入还是更新操作
        keepValueRes=MySqlUtils.queryKeepValueCheixId()
        SeriesExtPipeline.savedChexiIdSet=MySqlUtils.parseToIdSet(keepValueRes)
        # 初始化已爬取过且img不为空的车系id集合，用于判重，并决定是否再次爬取或更新
        savedChexiRes=MySqlUtils.querySavedImgChexi()
        SeriesExtPipeline.savedImgIdSet=MySqlUtils.parseToIdSet(savedChexiRes)

        # 初始化断点
        Point.init()
        # 切入断点
        SeriesExtPipeline.waitingCrawlIdSet=Point.cutInto(SeriesExtPipeline.chexiIdSet)





    def close_spider(self,spider):
        if len(self.imgItemList) > 0 :
            self.dbpool.runInteraction(self.update_img,self.imgItemList)
        if len(self.insertKeepValueItemList) > 0 :
            self.dbpool.runInteraction(self.insert_keepvalue, self.insertKeepValueItemList)
        if len(self.updateKeepValueItemList) > 0 :
            self.dbpool.runInteraction(self.update_keepValue,self.updateKeepValueItemList)
        print("本次更新图片%s次，保存保值率%s次，更新保值率%s次" % (self.imgUpdateCount,self.keepValueInsertCount,self.keepValueUpdateCount))

        # 断点功能记录已爬取的车系id到文件中
        Point.savePointFromSet(SeriesExtPipeline.crawledIdSet)

        # 断点判断是否正常爬取结束还是中断
        if len(SeriesExtPipeline.crawledIdSet) >= len(SeriesExtPipeline.waitingCrawlIdSet):
            # 正常爬取结束生成标识文件
            Point.complete()
        print("断点显示本次爬取%s,剩余爬取%s" % (len(SeriesExtPipeline.crawledIdSet),len(SeriesExtPipeline.waitingCrawlIdSet)-len(SeriesExtPipeline.crawledIdSet)))








