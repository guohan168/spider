
import pymysql
class MySqlUtils(object):
    #获取数据库链接
    vcar_host="10.1.11.129"
    @classmethod
    def getConnection(self):
        conn = pymysql.connect(host='localhost', user='root', passwd='root', db='vcar_vcyber_com', port=3306, charset='utf8')
        return conn

    @classmethod
    def queryBrandId(self):
        #self.log("start query --------------------------------")
        queryList=list()
        try:
            conn = self.getConnection()
            cur = conn.cursor()
            sql="""
            SELECT  `vcar_pinpai`.`pinpaiID`
            FROM `vcar_vcyber_com`.`vcar_pinpai`;
            """
            cur.execute(sql)
            res=cur.fetchall()
            #for item in res:
                #print(item)
                #self.log(item)
            #返回的是列表，列表元素类型是元组[(),(),,]
            return res

        except Exception as e:
            pass
            #print(e)
            #self.log(e)
            #self.log("查询失败")
        finally:
            cur.close()
            conn.close()
        #self.log("end query ----------------------------------")


    #查询车系信息，返回元组(brandId,seriesId,seriesLink)
    @classmethod
    def querySeriesLink(self):
        sql="""
                SELECT 
                    `vcar_chexi`.`pinpaiID`,
                    `vcar_chexi`.`chexiID`,
                    `vcar_chexi`.`url`
                FROM `vcar_vcyber_com`.`vcar_chexi`;
        """
        try:
            #获取数据连接
            conn=self.getConnection()
            #获取查询游标
            cursor=conn.cursor()
            #执行查询
            cursor.execute(sql)
            #获取结果
            res=cursor.fetchall()
            #for item in res:
                #print(item)
            return res
        except Exception as e:
            pass
        finally:
            conn.close()
            cursor.close()

    @classmethod
    def insertSpecItemList(cls,itemList):
        sql="""
                INSERT INTO `vcar_vcyber_com`.`vcar_chexing`
                    (`chexingID`,
                    `pinpaiID`,
                    `chexiID`,
                    `name`,
                    `url`)
                    VALUES
                    (%s,
                    %s,
                    %s,
                    %s,
                    %s);
            """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.executemany(sql,itemList)
            # 提交
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def querySpec(cls):
        sql="""
            SELECT 
                chexingID,
                chexiID,
                pinpaiID,
                name 
            FROM vcar_vcyber_com.vcar_chexing 
        """
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql)
            res=cursor.fetchall()
            return res
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()


    # 将车型元组集合转换为车型IDset集合
    @classmethod
    def parseToChexingIdSet(cls,res):
        chexingIdSet=set()
        for item in res:
            chexingIdSet.add(item[0])
        return chexingIdSet

    # 将车系元组集合转换成车系ID集合
    @classmethod
    def parseToSeriesIdSet(cls,res):
        seriesIdSet=set()
        for item in res:
            seriesIdSet.add(item[1])
        return seriesIdSet

    # 查询车系id集合中的车系数据
    @classmethod
    def findChexiInChexiSet(cls,seriesItems,seriesIdSet):
        waitingCrawlItems=list()
        for id in seriesIdSet:
             for item in seriesItems:
                 if id == item[1]:
                    waitingCrawlItems.append(item)
                    break
        return waitingCrawlItems;

    @classmethod
    def test(cls):
        print("start")
        sql="""
               UPDATE `vcar_vcyber_com`.`vcar_chexing`
               SET
                    `avgFuel` =  %s,
                    `numPeople` = %s,
                    `imgUrlS` = %s
                WHERE `chexingID` = %s;
        """
        params=(None,None,None,'1000')
        try:
            # 获取数据连接
            conn = cls.getConnection()
            # 获取查询游标
            cursor = conn.cursor()
            # 执行
            # print(itemList)
            cursor.execute(sql,params)
            # 提交
            conn.commit()
            print("commit")
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
            print("end")






MySqlUtils.test()
# res=my.queryExistChexingId()
# my.parseChexingIdTupeListToList(res)
# specList=[('1', 'h', 't', '2018款 118i 时尚型', 'https://www.autohome.com.cn/spec/33409/#pvareaid=2042128'), ('2', 'h', 't', '2018款 118i 运动型', 'https://www.autohome.com.cn/spec/33410/#pvareaid=2042128'), ('3', 'h', 't', '2018款 118i 设计套装型', 'https://www.autohome.com.cn/spec/32582/#pvareaid=2042128'), ('4', 'h', 't', '2018款 120i 设计套装型', 'https://www.autohome.com.cn/spec/33411/#pvareaid=2042128'), ('5', 'h', 't', '2018款 125i 运动型', 'https://www.autohome.com.cn/spec/33412/#pvareaid=2042128')]
# MySqlUtils.insertSpecItemList(specList)
