# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import SeriesItem,SpecItem
from .mySqlUtils import MySqlUtils
from scrapy.conf import settings
import pymysql
import pymysql.cursors
import scrapy
import xlwt
from twisted.enterprise import adbapi
from scrapy import log
from .point import Point


class SpecPipeline(object):
    count=0
    errorCount=0
    itmeList = list() # 用于批量插入数据库参数保存
    updateItemList=list() # 用于批量更新的参数集合
    chexingIdSet=set() # 用于判重
    existChexingIdSet=set() # 从数据库查询已存在的车型id集合
    errorModel = "{count:%s,class:%s,method:%s,errorInfo:%s}"

    # 已爬车系取计数器
    crawledSeriesCount=0
    # 新增车型数
    addSpecCount=0
    # 待爬车系ID集合
    waitingCrawlSeriesIdSet=None
    # 已爬车系id集合
    crawledSeriesIdSet=set()

    #通过构造函数设置属性
    def __init__(self,dbpool):
        self.dbpool=dbpool
        self.existChexingIdSet=MySqlUtils.parseToChexingIdSet(MySqlUtils.querySpec())


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

        if isinstance(item,SeriesItem):
            self.dbpool.runInteraction(self.updateSeriesItem,item)
        elif isinstance(item,SpecItem):
            if item['chexingID'] not in self.chexingIdSet:
                self.chexingIdSet.add(item['chexingID'])
                # 若车型ID存在于数据库中，则存入更新集合中,否则存入插入集合中
                if item['chexingID'] in self.existChexingIdSet:
                    self.updateItemList.append((item['pinpaiID'], item['chexiID'], item['name'], item['url'],item['chexingID']))
                else:
                    self.itmeList.append((item['chexingID'], item['pinpaiID'], item['chexiID'], item['name'], item['url']))
                self.count += 1
                if len(self.itmeList) >= 100:
                    # 执行数据库操作
                    paramsList=self.itmeList.copy() # 因为是异步操作保存，所以要进行复制，否则清空后就没有数据了
                    updateParamsList=self.updateItemList.copy()
                    self.itmeList.clear()
                    self.updateItemList.clear()
                    self.dbpool.runInteraction(self.insertSpecList,paramsList)
                    self.dbpool.runInteraction(self.updateSpec,updateParamsList)
        return item



    def insertSpecList(self,cusor,paramsList):
        try:
            #print("-------------->execute insert")
            insert_sql = """
                            INSERT INTO `vcar_vcyber_com`.`vcar_chexing`
                            (`chexingID`,
                            `pinpaiID`,
                            `chexiID`,
                            `name`,
                            `url`)
                            VALUES
                            (   %s,
                                %s,
                                %s,
                                %s,
                                %s);
                         """
            cusor.executemany(insert_sql, paramsList)
            print("save--------------------------------------->%s" % self.count)
        except Exception as e:
            print(e)
            print(paramsList)
            self.errorCount += 1
            filename = "/Users/guohan/DeskTop/mySqlError.txt"
            error = self.errorModel % (self.errorCount, "piplines", "insertSpecList", str(e))
            with open(filename, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(error)
                f.flush()
                f.close()
    # 更新车系
    def updateSpec(self,cursor,updateParamsList):
        update_sql="""
                UPDATE `vcar_vcyber_com`.`vcar_chexing`
                SET
                    `pinpaiID` = %s,
                    `chexiID` = %s,
                    `name` = %s,
                    `url` = %s
                WHERE `chexingID` = %s;
        """
        try:
            cursor.executemany(update_sql, updateParamsList)
            print("update--------------------------------------->%s" % self.count)
        except Exception as e:
            print(e)
            print(updateParamsList)
            self.errorCount += 1
            filename = "/Users/guohan/DeskTop/mySqlError.txt"
            error = self.errorModel % (self.errorCount, "piplines", "updateSpec", str(e))
            with open(filename, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
                f.write(error)
                f.flush()
                f.close()



    #更新车系信息：最小价格、最大价格、车系评分、级别
    def updateSeriesItem(self,cursor,item):
        update_sql,params=item.get_update_sql()
        cursor.execute(update_sql,params)
    #
    # def insertSpecItem(self,cursor,item):
    #     insert_sql,params=item.get_insert_sql()
    #     cursor.execute(insert_sql,item)

    def open_spider(self,spider):
        # 查询所有车系id集合
        res=MySqlUtils.querySeriesLink()
        totalSeriesIdSet=MySqlUtils.parseToSeriesIdSet(res)
        # 初始化断点
        Point.init()
        # 切入断点
        SpecPipeline.waitingCrawlSeriesIdSet=Point.cutInto(totalSeriesIdSet)


    def close_spider(self,spider):
        print("------------------------------------------------------------------------------------------> close")
        self.dbpool.runInteraction(self.insertSpecList,self.itmeList)
        # 如果爬取完成则生成断点文件，否则保存断点内容
        # 向断点续爬文件中写入已爬车型id
        crawledIdStr = ""
        for id in SpecPipeline.crawledSeriesIdSet:
            crawledIdStr += id + ","
        Point.savePoint(crawledIdStr)
        print("断点显示已爬取%s,剩余爬取%s，新增车型%s" % (SpecPipeline.crawledSeriesCount, len(SpecPipeline.waitingCrawlSeriesIdSet) - len(SpecPipeline.crawledSeriesIdSet),SpecPipeline.addSpecCount))
        # 如果正常爬取结束，则在temp目录下写入over.txt 标识文件
        if SpecPipeline.crawledSeriesCount >= len(SpecPipeline.waitingCrawlSeriesIdSet):
            Point.complete()




