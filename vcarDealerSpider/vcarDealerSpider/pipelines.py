# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .mySqlUtils import MySqlUtils
from scrapy.conf import settings
import pymysql
import pymysql.cursors
import scrapy
import xlwt
import datetime
from twisted.enterprise import adbapi
from scrapy import log
from .items import DealerItem

class DealerPipeline(object):
    # 经销商id字符串拼接
    idStr=""
    # 经销商集合
    dealerList=list()
    # 插入经销商集合
    insertDealerList=list()

    # 更新经销商集合
    updateDealerList=list()

    # 保存经销商计数器
    saveCount=0
    # 更新经销商计数器
    updateCount=0



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

    # 通过构造函数设置属性
    def __init__(self, dbpool):
        self.dbpool = dbpool




    # 主方法
    def process_item(self, item, spider):
        self.dealerList.append(item)
        if len(self.dealerList) > 100 :
            self.save(self.dealerList.copy())
            self.dealerList.clear()

        return item


    # 插入经销商
    def insertDealers(self,cursor,paramsList):
        try:
            cursor.executemany(MySqlUtils.sql_insert_dealer,paramsList)
        except Exception as e:
            print(e)


    # 更新经销商
    def updateDealers(self,cursor,paramsList):
        try:
            cursor.executemany(MySqlUtils.sql_update_dealer,paramsList)
        except Exception as e:
            print(e)


    def save(self,dealerList):
        # 判重，找出已存在的和未存在的，分类放入集合中
        idStr = ""
        idSet = set()
        for item in dealerList:
            idStr += item['sid'] + ","
            idSet.add(item['sid'])
        idStr = idStr[:len(idStr)-1]
        # 查询数据库中已存在的id集合
        existDealerRes=MySqlUtils.query(MySqlUtils.sql_query_dealer_in % idStr)
        existDealerIdSet=MySqlUtils.parseToSet(existDealerRes,0)
        unExistIdSet = idSet - existDealerIdSet
        insertList=list()
        updateList=list()
        # 找出已经存在于数据库中的经销商
        for item in dealerList:
            if item['sid'] in unExistIdSet:
                insertParams=(item['sid'],item['dealerName'],item['homepageUrl'],item['headImgUrl'],item['provinceCode'],item['province'],item['city'],item['cityCode'],item['county'],item['countyCode'],item['mainBrand'],item['mainBrandId'],item['tel'],item['detailAddr'],item['onSaleNum'],item['type'],item['badge'],item['limitAreaType'],item['limitAreaDetail'])
                # print(insertParams)
                insertList.append(insertParams)
            else :
                updateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                updateParams=(item['dealerName'],item['homepageUrl'],item['headImgUrl'],item['provinceCode'],item['province'],item['city'],item['cityCode'],item['county'],item['countyCode'],item['mainBrand'],item['mainBrandId'],item['tel'],item['detailAddr'],item['onSaleNum'],item['type'],item['badge'],item['limitAreaType'],item['limitAreaDetail'],updateTime,item['sid'])
                updateList.append(updateParams)
        # 插入经销商
        if len(insertList) > 0:
            # self.dbpool.runInteraction(self.insertDealers,insertList)
            MySqlUtils.updateList(MySqlUtils.sql_insert_dealer,insertList)
            self.saveCount += len(insertList)
        # 更新经销商
        if len(updateList) > 0:
            # self.dbpool.runInteraction(self.updateDealers,updateList)
            MySqlUtils.updateList(MySqlUtils.sql_update_dealer,updateList)
            self.updateCount += len(updateList)
        print("---------------------------------------------------->saveCount:%s ,updateCount:%s" % (self.saveCount,self.updateCount))






    # scrapy生命周期方法，打开爬虫
    def open_spider(self, spider):

        pass


    # scrapy生命周期方法，关闭爬虫
    def close_spider(self,spider):
        self.save(self.dealerList)

        pass
