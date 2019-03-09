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
from twisted.enterprise import adbapi
from scrapy import log
from .point import Point
from .items import UserItem

class UserPipeline(object):

    # 用户item缓存
    updateUserList=list()
    # 初始化爬取用户数
    initUserCount=0
    # 统计用户更新次数
    updateUserCount=0
    # 记录当前断点用户
    currentUserId=None

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


    # scrapy生命周期方法，打开爬虫
    def open_spider(self,spider):

        pass

    # 从scrapy 流转过来的数据到此处进行处理
    def process_item(self, item, spider):
        self.currentUserId=item['sid']
        self.updateUserCount += 1
        # 采用异步批量保存到数据库
        updateParams=(item['headImg'],item['sex'],item['province'],item['provinceCode'],item['city'],item['cityCode'],item['level'],item['focusNum'],item['fansNum'],item['vStatus'],item['updateTime'],item['sid'])
        self.updateUserList.append(updateParams)
        if len(self.updateUserList) > 50:
            self.dbpool.runInteraction(self.updateUser, self.updateUserList.copy())
            self.updateUserList.clear()
        return item

    def updateUser(self,cursor,paramsList):
        try:
            cursor.executemany(MySqlUtils.sql_update_user, paramsList)
            print("updateUser--------------------------------------->%s" % self.updateUserCount)
            Point.clearAndSavePoint(self.currentUserId)
        except Exception as e:
            print(e)


    # scrapy生命周期方法，关闭爬虫
    def close_spider(self,spider):
        # 先保存未更新到数据库中的用户集合
        if len(self.updateUserList) > 0:
            self.dbpool.runInteraction(self.updateUser, self.updateUserList.copy())
        # 解析完成，将用户id写入断点文件，写入之前要清除上一次的所有id集合,此行代码后期要移动到pipeline生命周期函数process和close中
        print("cclllllllllllllllloooooooooooooooossssssssssseeeeee:%s" % self.currentUserId)
        Point.clearAndSavePoint(self.currentUserId)
        # 如果更新次数等于初始爬取次数，则爬取结束
        if self.updateUserCount == int(UserPipeline.initUserCount):
            Point.complete()



